"""
config/settings.py
------------------
Central configuration for the AI Legal Aid Multi-Agent System.
All sensitive values are loaded from environment variables via .env.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── IBM watsonx.ai settings ────────────────────────────────────────────────
WATSONX_API_KEY    = os.getenv("WATSONX_API_KEY", "")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_URL        = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# IBM Granite model — reliable, instruction-tuned, responsible AI
GRANITE_MODEL_ID   = "ibm/granite-3-3-8b-instruct"

# Generation parameters — low temperature for factual legal information
GRANITE_PARAMS = {
    "decoding_method": "greedy",
    "max_new_tokens": 900,
    "min_new_tokens": 80,
    "temperature": 0.25,
    "repetition_penalty": 1.1,
}

# ── Flask settings ─────────────────────────────────────────────────────────
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
FLASK_DEBUG      = os.getenv("FLASK_DEBUG", "false").lower() == "true"
FLASK_HOST       = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT       = int(os.getenv("FLASK_PORT", "5000"))

# ── Demo mode (runs without a real API key, uses pre-built responses) ──────
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# ── Legal issue categories ─────────────────────────────────────────────────
LEGAL_CATEGORIES = [
    "Housing & Tenant Rights",
    "Employment & Workplace",
    "Family Law & Divorce",
    "Immigration & Visa",
    "Criminal Law",
    "Consumer Rights",
    "Civil Rights & Discrimination",
    "Debt & Bankruptcy",
    "Healthcare & Medical Rights",
    "Education Rights",
    "Small Business & Contracts",
    "Other / General Legal Query",
]

# ── Supported countries (representative list) ─────────────────────────────
SUPPORTED_COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Australia",
    "India", "Germany", "France", "South Africa", "Nigeria",
    "Brazil", "Mexico", "Philippines", "New Zealand", "Ireland",
    "Singapore", "Pakistan", "Bangladesh", "Kenya", "Ghana",
    "Other",
]
