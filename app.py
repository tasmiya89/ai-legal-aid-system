"""
app.py
------
AI Legal Aid Multi-Agent System — Flask Application Entry Point
----------------------------------------------------------------
Orchestrates the 4-agent pipeline:
  1. Query Understanding Agent
  2. Legal Research Agent
  3. Document Analysis Agent
  4. Legal Aid Finder Agent

All routes include ethical guardrails, input sanitisation,
and mandatory legal disclaimers on every response.

IBM Granite LLM powers all AI agents via IBM watsonx.ai.
"""

import logging
import time
from flask import Flask, render_template, request, jsonify
from config.settings import (
    FLASK_SECRET_KEY, FLASK_DEBUG, FLASK_HOST, FLASK_PORT,
    LEGAL_CATEGORIES, SUPPORTED_COUNTRIES
)
from utils.sanitizer import validate_query
from utils.disclaimer import LEGAL_DISCLAIMER, CRISIS_RESOURCES, SHORT_DISCLAIMER
import agents.query_understanding as agent1
import agents.legal_research      as agent2
import agents.document_analysis   as agent3
import agents.legal_aid_finder    as agent4

# ── Logging configuration ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Flask app setup ────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY


# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main web interface."""
    return render_template(
        "index.html",
        legal_categories=LEGAL_CATEGORIES,
        supported_countries=SUPPORTED_COUNTRIES,
    )


@app.route("/api/legal-query", methods=["POST"])
def legal_query():
    """
    Main API endpoint — orchestrates the full 4-agent pipeline.

    Expected JSON body:
    {
        "country": "United States",
        "state": "California",
        "issue_category": "Housing & Tenant Rights",
        "description": "My landlord is trying to evict me without notice."
    }

    Returns JSON with each agent's output, the combined report,
    crisis flag, and mandatory legal disclaimer.
    """
    start_time = time.time()

    # ── 1. Parse request ───────────────────────────────────────────────────
    data = request.get_json(silent=True) or {}
    country        = data.get("country", "").strip()
    state          = data.get("state", "").strip()
    issue_category = data.get("issue_category", "").strip()
    description    = data.get("description", "").strip()

    logger.info(
        "Legal query received — country=%s, issue=%s",
        country, issue_category
    )

    # ── 2. Validate and sanitise inputs ────────────────────────────────────
    validation = validate_query(country, state, issue_category, description)

    if not validation["valid"]:
        return jsonify({
            "success": False,
            "errors": validation["errors"],
            "disclaimer": SHORT_DISCLAIMER,
        }), 400

    # Use sanitised values from here on
    clean = validation["sanitized"]
    country_s   = clean["country"]
    state_s     = clean["state"]
    category_s  = clean["issue_category"]
    desc_s      = clean["description"]
    crisis      = validation["crisis"]

    # ── 3. Run Agent 1 — Query Understanding ──────────────────────────────
    logger.info("Running Agent 1: Query Understanding")
    try:
        agent1_output = agent1.run(country_s, state_s, category_s, desc_s)
    except Exception as exc:
        logger.error("Agent 1 failed: %s", exc)
        agent1_output = f"Unable to analyse query: {exc}"

    # ── 4. Run Agent 2 — Legal Research ───────────────────────────────────
    logger.info("Running Agent 2: Legal Research")
    try:
        agent2_output = agent2.run(agent1_output, country_s, state_s, category_s)
    except Exception as exc:
        logger.error("Agent 2 failed: %s", exc)
        agent2_output = f"Unable to complete legal research: {exc}"

    # ── 5. Run Agent 3 — Document Analysis ────────────────────────────────
    logger.info("Running Agent 3: Document Analysis")
    try:
        agent3_output = agent3.run(agent1_output, agent2_output, country_s, state_s, category_s)
    except Exception as exc:
        logger.error("Agent 3 failed: %s", exc)
        agent3_output = f"Unable to complete document analysis: {exc}"

    # ── 6. Run Agent 4 — Legal Aid Finder ─────────────────────────────────
    logger.info("Running Agent 4: Legal Aid Finder")
    try:
        agent4_output = agent4.run(agent1_output, country_s, state_s, category_s)
    except Exception as exc:
        logger.error("Agent 4 failed: %s", exc)
        agent4_output = f"Unable to find legal aid resources: {exc}"

    elapsed = round(time.time() - start_time, 2)
    logger.info("Pipeline completed in %.2fs", elapsed)

    # ── 7. Assemble response ───────────────────────────────────────────────
    response_payload = {
        "success": True,
        "jurisdiction": f"{state_s}, {country_s}" if state_s else country_s,
        "issue_category": category_s,
        "crisis": crisis,
        "agents": {
            "query_understanding": {
                "title": "🔍 Query Understanding",
                "subtitle": "How your legal question was understood",
                "output": agent1_output,
            },
            "legal_research": {
                "title": "📚 Legal Research",
                "subtitle": "Applicable laws, statutes, and rights",
                "output": agent2_output,
            },
            "document_analysis": {
                "title": "📄 Plain-Language Explanation",
                "subtitle": "What this means for you in simple terms",
                "output": agent3_output,
            },
            "legal_aid_finder": {
                "title": "🤝 Legal Aid Resources",
                "subtitle": "Free and low-cost legal help near you",
                "output": agent4_output,
            },
        },
        "crisis_resources": CRISIS_RESOURCES if crisis else None,
        "disclaimer": LEGAL_DISCLAIMER,
        "processing_time_seconds": elapsed,
        "powered_by": "IBM Granite 3.3 8B Instruct via IBM watsonx.ai",
    }

    return jsonify(response_payload)


@app.route("/api/health")
def health():
    """Health check endpoint."""
    from config.settings import WATSONX_API_KEY, DEMO_MODE
    return jsonify({
        "status": "healthy",
        "service": "AI Legal Aid Multi-Agent System",
        "model": "IBM Granite 3.3 8B Instruct",
        "demo_mode": DEMO_MODE or not WATSONX_API_KEY or WATSONX_API_KEY == "your_ibm_watsonx_api_key_here",
        "version": "1.0.0",
    })


@app.route("/api/categories")
def get_categories():
    """Return available legal issue categories."""
    return jsonify({"categories": LEGAL_CATEGORIES})


@app.route("/api/countries")
def get_countries():
    """Return supported countries."""
    return jsonify({"countries": SUPPORTED_COUNTRIES})


# ── Error handlers ─────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found", "disclaimer": SHORT_DISCLAIMER}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error("Internal server error: %s", e)
    return jsonify({
        "error": "An internal error occurred. Please try again.",
        "disclaimer": SHORT_DISCLAIMER,
    }), 500


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from config.settings import DEMO_MODE, WATSONX_API_KEY
    demo = DEMO_MODE or not WATSONX_API_KEY or WATSONX_API_KEY == "your_ibm_watsonx_api_key_here"

    print("=" * 65)
    print("  AI Legal Aid Multi-Agent System")
    print("  Powered by IBM Granite LLM | IBM watsonx.ai")
    print("=" * 65)
    if demo:
        print("  [!] Running in DEMO MODE (no real API key configured)")
        print("      Set WATSONX_API_KEY in .env to enable live AI responses")
    else:
        print("  [OK] IBM watsonx.ai API key configured")
    print(f"  [->] Open browser at: http://{FLASK_HOST}:{FLASK_PORT}")
    print("=" * 65)

    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
    )
