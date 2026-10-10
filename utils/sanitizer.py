"""
utils/sanitizer.py
------------------
Input sanitisation and guardrail utilities.
Protects against prompt injection, XSS, and out-of-domain queries.
Implements AI ethics guardrail — no PII storage, safe content only.
"""

import re
import bleach
import logging

logger = logging.getLogger(__name__)

# ── Prompt injection patterns ──────────────────────────────────────────────
_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?previous",
    r"you\s+are\s+now\s+(?:a|an)\s+",
    r"act\s+as\s+(?:a|an)\s+",
    r"pretend\s+(you\s+are|to\s+be)",
    r"jailbreak",
    r"DAN\s+mode",
    r"<script",
    r"javascript:",
    r"system\s*prompt",
    r"override\s+instructions",
]

# ── Crisis / emergency keywords ────────────────────────────────────────────
_CRISIS_KEYWORDS = [
    "domestic violence", "abuse", "threatened", "unsafe", "danger",
    "hurt me", "hurt myself", "suicide", "self-harm", "emergency",
    "assault", "stalking", "harassment", "beaten",
]

# ── Out-of-domain patterns (non-legal topics) ──────────────────────────────
_OFF_DOMAIN_PATTERNS = [
    r"\b(recipe|cooking|sport[s]?|weather|music|movie|game[s]?)\b",
]

ALLOWED_HTML_TAGS: list = []  # No HTML allowed in user inputs


def sanitize_input(text: str) -> str:
    """
    Sanitise a user-provided string:
    1. Strip HTML tags
    2. Remove prompt injection patterns
    3. Trim to maximum safe length
    """
    if not text:
        return ""

    # Strip HTML
    cleaned = bleach.clean(str(text), tags=ALLOWED_HTML_TAGS, strip=True)

    # Remove injection patterns
    for pattern in _INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            logger.warning("Prompt injection pattern detected and removed.")
            cleaned = re.sub(pattern, "[REMOVED]", cleaned, flags=re.IGNORECASE)

    # Limit length (prevents token flooding)
    cleaned = cleaned[:2000].strip()

    return cleaned


def check_crisis_keywords(text: str) -> bool:
    """Return True if crisis/emergency keywords are detected."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in _CRISIS_KEYWORDS)


def is_legal_domain(issue_category: str, description: str) -> bool:
    """
    Basic check: is this query reasonably within the legal aid domain?
    Returns False only for clearly off-topic queries.
    """
    # If a recognised legal category was selected, it's always in-domain
    if issue_category and issue_category != "Other / General Legal Query":
        return True

    combined = (issue_category + " " + description).lower()
    for pattern in _OFF_DOMAIN_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            return False

    return True


def validate_query(country: str, state: str, issue_category: str, description: str) -> dict:
    """
    Validate all user inputs. Returns a dict with:
    - 'valid': bool
    - 'errors': list[str]
    - 'crisis': bool
    - 'sanitized': dict of cleaned fields
    """
    errors = []

    country_clean    = sanitize_input(country)
    state_clean      = sanitize_input(state)
    category_clean   = sanitize_input(issue_category)
    description_clean = sanitize_input(description)

    if not country_clean:
        errors.append("Please select your country.")
    if not category_clean:
        errors.append("Please select a legal issue category.")

    crisis_detected = check_crisis_keywords(description_clean)

    if not is_legal_domain(category_clean, description_clean):
        errors.append(
            "This system is designed for legal queries only. "
            "Please describe your legal issue or select an appropriate category."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "crisis": crisis_detected,
        "sanitized": {
            "country": country_clean,
            "state": state_clean,
            "issue_category": category_clean,
            "description": description_clean,
        },
    }
