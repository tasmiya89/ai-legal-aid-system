/**
 * app.js
 * ------
 * AI Legal Aid System — Frontend Application
 * Powered by IBM Granite LLM
 *
 * Handles:
 * - Form validation and submission
 * - Agent pipeline progress simulation
 * - Result rendering (Markdown-like formatting)
 * - Accordion interactions
 * - Accessibility (ARIA states, focus management)
 * - Crisis banner display
 * - Character counter
 */

"use strict";

/* ── DOM References ─────────────────────────────────────────────────────── */
const form            = document.getElementById("legalQueryForm");
const countrySelect   = document.getElementById("country");
const stateInput      = document.getElementById("state");
const categorySelect  = document.getElementById("issueCategory");
const descTextarea    = document.getElementById("description");
const descCount       = document.getElementById("descCount");
const submitBtn       = document.getElementById("submitBtn");
const progressSection = document.getElementById("progressSection");
const progressSubtitle= document.getElementById("progressSubtitle");
const resultsSection  = document.getElementById("resultsSection");
const errorSection    = document.getElementById("errorSection");
const errorMessage    = document.getElementById("errorMessage");
const crisisBanner    = document.getElementById("crisisBanner");
const newQueryBtn     = document.getElementById("newQueryBtn");
const retryBtn        = document.getElementById("retryBtn");
const demoBadge       = document.getElementById("demoBadge");
const liveBadge       = document.getElementById("liveBadge");

/* ── Agent step definitions ─────────────────────────────────────────────── */
const AGENT_STEPS = [
    { id: "step1", label: "Agent 1: Query Understanding", delay: 800 },
    { id: "step2", label: "Agent 2: Legal Research",      delay: 1600 },
    { id: "step3", label: "Agent 3: Document Analysis",   delay: 2400 },
    { id: "step4", label: "Agent 4: Legal Aid Finder",    delay: 3200 },
];

/* ── On load ────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
    checkDemoMode();
    initCharCounter();
    initAccordions();
    newQueryBtn.addEventListener("click", resetToForm);
    retryBtn.addEventListener("click", resetToForm);
});

/* ── Health check to show demo/live badge ───────────────────────────────── */
async function checkDemoMode() {
    try {
        const res  = await fetch("/api/health");
        const data = await res.json();
        if (data.demo_mode) {
            demoBadge.style.display = "inline-block";
            liveBadge.style.display = "none";
        } else {
            demoBadge.style.display = "none";
            liveBadge.style.display = "inline-block";
        }
    } catch (_) {
        // Keep default
    }
}

/* ── Character counter ──────────────────────────────────────────────────── */
function initCharCounter() {
    descTextarea.addEventListener("input", () => {
        const len = descTextarea.value.length;
        const max = 2000;
        descCount.textContent = `${len} / ${max}`;
        descCount.className = "char-count";
        if (len > 1800) descCount.classList.add("warning");
        if (len > 1950) { descCount.classList.remove("warning"); descCount.classList.add("danger"); }
    });
}

/* ── Form submission ────────────────────────────────────────────────────── */
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    const payload = {
        country:        countrySelect.value.trim(),
        state:          stateInput.value.trim(),
        issue_category: categorySelect.value.trim(),
        description:    descTextarea.value.trim(),
    };

    showProgress();
    animateSteps();

    try {
        const response = await fetch("/api/legal-query", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            const errMsg = data.errors
                ? data.errors.join(" ")
                : (data.error || "An error occurred. Please try again.");
            showError(errMsg);
            return;
        }

        showResults(data);

    } catch (err) {
        console.error("Fetch error:", err);
        showError(
            "Could not connect to the AI service. " +
            "Please check your internet connection and try again."
        );
    }
});

/* ── Form validation ────────────────────────────────────────────────────── */
function validateForm() {
    let valid = true;

    // Country
    const countryErr = document.getElementById("countryError");
    if (!countrySelect.value) {
        countryErr.textContent = "Please select your country.";
        countrySelect.classList.add("error");
        valid = false;
    } else {
        countryErr.textContent = "";
        countrySelect.classList.remove("error");
    }

    // Category
    const catErr = document.getElementById("categoryError");
    if (!categorySelect.value) {
        catErr.textContent = "Please select a legal issue category.";
        categorySelect.classList.add("error");
        valid = false;
    } else {
        catErr.textContent = "";
        categorySelect.classList.remove("error");
    }

    if (!valid) {
        // Focus first error
        if (!countrySelect.value) countrySelect.focus();
        else categorySelect.focus();
    }

    return valid;
}

/* ── Progress display ───────────────────────────────────────────────────── */
function showProgress() {
    form.parentElement.style.display = "none";   // hide form card
    progressSection.style.display   = "block";
    resultsSection.style.display    = "none";
    errorSection.style.display      = "none";
    crisisBanner.style.display      = "none";

    // Reset all steps
    AGENT_STEPS.forEach(s => {
        const el = document.getElementById(s.id);
        el.classList.remove("active", "done");
        el.querySelector(".step-status").textContent = "Waiting…";
    });

    progressSubtitle.textContent = "Sending your query to the AI agent pipeline…";
    submitBtn.disabled = true;

    // Scroll to progress
    progressSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

/* ── Animate step indicators (cosmetic — reflects real pipeline flow) ────── */
function animateSteps() {
    AGENT_STEPS.forEach((step, idx) => {
        setTimeout(() => {
            // Mark previous as done
            if (idx > 0) {
                const prev = document.getElementById(AGENT_STEPS[idx - 1].id);
                prev.classList.remove("active");
                prev.classList.add("done");
                prev.querySelector(".step-status").textContent = "✓ Done";
            }
            // Mark current as active
            const cur = document.getElementById(step.id);
            cur.classList.add("active");
            cur.querySelector(".step-status").textContent = "Running…";
            progressSubtitle.textContent = `${step.label} is working…`;
        }, step.delay);
    });
}

/* ── Mark all steps done (called when results arrive) ───────────────────── */
function markAllStepsDone() {
    AGENT_STEPS.forEach(s => {
        const el = document.getElementById(s.id);
        el.classList.remove("active");
        el.classList.add("done");
        el.querySelector(".step-status").textContent = "✓ Done";
    });
}

/* ── Show results ───────────────────────────────────────────────────────── */
function showResults(data) {
    markAllStepsDone();

    setTimeout(() => {
        progressSection.style.display = "none";
        resultsSection.style.display  = "block";

        // Crisis banner
        if (data.crisis) {
            crisisBanner.style.display = "block";
        }

        // Header meta
        document.getElementById("resultsJurisdiction").textContent =
            "📍 " + (data.jurisdiction || "");
        document.getElementById("resultsCategory").textContent =
            "⚖️ " + (data.issue_category || "");
        document.getElementById("resultsTime").textContent =
            `⏱ ${data.processing_time_seconds}s`;

        // Populate each agent card
        const agents = data.agents || {};
        populateAgentCard(1, agents.query_understanding);
        populateAgentCard(2, agents.legal_research);
        populateAgentCard(3, agents.document_analysis);
        populateAgentCard(4, agents.legal_aid_finder);

        // Disclaimer
        const disclaimerText = document.getElementById("disclaimerText");
        disclaimerText.innerHTML = `<div class="agent-output">${escapeHtml(data.disclaimer || "")}</div>`;

        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 600);
}

function populateAgentCard(num, agentData) {
    if (!agentData) return;
    document.getElementById(`agentTitle${num}`).textContent    = agentData.title    || "";
    document.getElementById(`agentSubtitle${num}`).textContent = agentData.subtitle || "";
    document.getElementById(`agentOutput${num}`).innerHTML     = formatOutput(agentData.output || "");
}

/* ── Show error ─────────────────────────────────────────────────────────── */
function showError(message) {
    progressSection.style.display = "none";
    errorSection.style.display    = "block";
    errorMessage.textContent      = message;
    errorSection.scrollIntoView({ behavior: "smooth", block: "start" });
    submitBtn.disabled = false;
}

/* ── Reset to form ──────────────────────────────────────────────────────── */
function resetToForm() {
    resultsSection.style.display  = "none";
    errorSection.style.display    = "none";
    progressSection.style.display = "none";
    crisisBanner.style.display    = "none";
    form.parentElement.style.display = "block";
    submitBtn.disabled = false;
    form.parentElement.scrollIntoView({ behavior: "smooth", block: "start" });
}

/* ── Accordion ──────────────────────────────────────────────────────────── */
function initAccordions() {
    document.querySelectorAll(".agent-card-header").forEach(header => {
        header.addEventListener("click", () => {
            const expanded = header.getAttribute("aria-expanded") === "true";
            const bodyId   = header.getAttribute("aria-controls");
            const body     = document.getElementById(bodyId);

            header.setAttribute("aria-expanded", String(!expanded));
            if (body) {
                body.hidden = expanded;
            }
        });
    });
}

/* ── Format output (lightweight Markdown → HTML) ───────────────────────── */
function formatOutput(text) {
    if (!text) return "";

    let html = escapeHtml(text);

    // Bold: **text** or __text__
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/__(.+?)__/g, "<strong>$1</strong>");

    // Italic: *text* or _text_
    html = html.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, "<em>$1</em>");

    // Headings: ## Heading → <h2>, ### → <h3>
    html = html.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
    html = html.replace(/^### (.+)$/gm,  "<h3>$1</h3>");
    html = html.replace(/^## (.+)$/gm,   "<h2>$1</h2>");
    html = html.replace(/^# (.+)$/gm,    "<h1>$1</h1>");

    // Unordered lists (lines starting with - or • or *)
    html = html.replace(/^[-•*] (.+)$/gm, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>(\n|$))+/g, m => `<ul>${m}</ul>`);

    // Ordered lists (lines starting with 1. 2. etc.)
    html = html.replace(/^\d+\. (.+)$/gm, "<li>$1</li>");

    // URLs → clickable links (but only if not already in an anchor tag)
    html = html.replace(
        /(?<!['"=])(https?:\/\/[^\s<>"']+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );

    // Line breaks: double newline → paragraph, single → <br>
    const lines = html.split(/\n\n+/);
    html = lines.map(block => {
        block = block.trim();
        if (!block) return "";
        // Don't wrap block-level elements in <p>
        if (/^<(h[1-6]|ul|ol|li|blockquote|div)/.test(block)) return block;
        return `<p>${block.replace(/\n/g, "<br>")}</p>`;
    }).join("\n");

    return html;
}

/* ── Safe HTML escaping ─────────────────────────────────────────────────── */
function escapeHtml(str) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}
