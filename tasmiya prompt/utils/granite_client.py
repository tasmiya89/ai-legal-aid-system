"""
utils/granite_client.py
-----------------------
IBM watsonx.ai client wrapper for IBM Granite LLM.
Provides a clean interface for all agent calls with retry logic
and graceful degradation when the API is unavailable.
"""

import os
import logging
from config.settings import (
    WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL,
    GRANITE_MODEL_ID, GRANITE_PARAMS, DEMO_MODE
)

logger = logging.getLogger(__name__)


def _get_model():
    """Instantiate and return the IBM Granite model client."""
    try:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference

        credentials = Credentials(
            api_key=WATSONX_API_KEY,
            url=WATSONX_URL,
        )
        model = ModelInference(
            model_id=GRANITE_MODEL_ID,
            credentials=credentials,
            project_id=WATSONX_PROJECT_ID,
            params=GRANITE_PARAMS,
        )
        return model
    except Exception as exc:
        logger.error("Failed to initialise IBM Granite model: %s", exc)
        raise


def call_granite(prompt: str, system_prompt: str = "") -> str:
    """
    Send a prompt to IBM Granite and return the generated text.

    Parameters
    ----------
    prompt        : The user-facing instruction / question for this agent turn.
    system_prompt : Optional system-level context that sets the agent's role.

    Returns
    -------
    str : Generated text from IBM Granite, or a fallback message.
    """
    if DEMO_MODE or not WATSONX_API_KEY or WATSONX_API_KEY == "your_ibm_watsonx_api_key_here":
        logger.warning("DEMO_MODE active — returning simulated response.")
        return _demo_response(prompt)

    full_prompt = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt

    try:
        model = _get_model()
        response = model.generate_text(prompt=full_prompt)
        return response.strip() if isinstance(response, str) else str(response).strip()
    except Exception as exc:
        logger.error("IBM Granite API call failed: %s", exc)
        return (
            "⚠️ The AI service is temporarily unavailable. "
            "Please try again in a few moments, or consult a qualified legal professional directly."
        )


def _demo_response(prompt: str) -> str:
    """
    Return a structured demo response when running without a real API key.
    This ensures the application is fully functional for demonstration purposes.
    """
    prompt_lower = prompt.lower()

    if "understand" in prompt_lower or "classify" in prompt_lower or "intent" in prompt_lower:
        return (
            "**Legal Query Classification (Demo)**\n\n"
            "- **Issue Category**: Housing & Tenant Rights\n"
            "- **Jurisdiction**: United States — California\n"
            "- **Core Legal Question**: Rights and remedies available to a tenant facing unlawful eviction\n"
            "- **Urgency Level**: Medium — no immediate crisis detected\n"
            "- **Key Legal Concepts**: Unlawful detainer, notice requirements, habitability standards, security deposit\n"
            "- **Recommended Focus Areas**: California Civil Code §1940-1954, local rent control ordinances"
        )
    elif "research" in prompt_lower or "law" in prompt_lower or "statute" in prompt_lower:
        return (
            "**Legal Research Summary (Demo)**\n\n"
            "**Applicable Laws & Statutes:**\n"
            "1. California Civil Code §1940–1954.1 — Landlord/Tenant obligations and habitability\n"
            "2. California Code of Civil Procedure §1161 — Unlawful detainer (eviction) procedures\n"
            "3. California Civil Code §1950.5 — Security deposit rules (max 2 months for unfurnished)\n"
            "4. AB 1482 (Tenant Protection Act 2019) — Just cause eviction protections\n\n"
            "**Key Rights:**\n"
            "- Tenant must receive written notice (3-day, 30-day, or 60-day depending on circumstances)\n"
            "- Landlord cannot self-help evict (change locks, remove belongings without court order)\n"
            "- Tenant has right to habitable premises\n\n"
            "**Official Sources:**\n"
            "- California Courts: https://www.courts.ca.gov/selfhelp-eviction.htm\n"
            "- CA Legislative Info: https://leginfo.legislature.ca.gov"
        )
    elif "analys" in prompt_lower or "plain" in prompt_lower or "explain" in prompt_lower:
        return (
            "**Plain-Language Analysis (Demo)**\n\n"
            "**What This Means For You:**\n\n"
            "In simple terms, if you are a tenant in California being asked to leave:\n\n"
            "✅ **You have strong protections.** Your landlord cannot simply remove you from your home without "
            "following a specific legal process that involves written notices and a court hearing.\n\n"
            "✅ **Written notice is required.** Depending on the reason (non-payment, lease violation, no fault), "
            "your landlord must give you a 3-day, 30-day, or 60-day written notice.\n\n"
            "✅ **Court process required.** If you don't leave after the notice, the landlord must file an "
            "unlawful detainer lawsuit in court. You have the right to respond and appear in court.\n\n"
            "⚠️ **Act quickly.** Court timelines are short (often 5 business days to respond after being served). "
            "Contact a legal aid organisation immediately if you receive court papers.\n\n"
            "✅ **Security deposit.** Your landlord must return your deposit within 21 days of move-out, "
            "with an itemised statement of any deductions."
        )
    else:
        return (
            "**Legal Aid Resources (Demo)**\n\n"
            "**Free & Low-Cost Legal Help Near You:**\n\n"
            "🏛️ **Legal Aid Society of San Francisco**\n"
            "   - Website: https://sflas.org | Phone: (415) 982-1300\n"
            "   - Speciality: Housing, tenant rights, eviction defence\n\n"
            "🏛️ **Bay Area Legal Aid**\n"
            "   - Website: https://baylegal.org | Phone: (415) 982-1300\n"
            "   - Speciality: Low-income civil legal services\n\n"
            "🏛️ **California Courts Self-Help Centre**\n"
            "   - Website: https://www.courts.ca.gov/selfhelp.htm\n"
            "   - Free: Forms, guides, and legal information\n\n"
            "🏛️ **LawHelpCA**\n"
            "   - Website: https://www.lawhelp.org/ca\n"
            "   - Free legal information and referrals statewide\n\n"
            "📞 **State Bar of California Lawyer Referral**\n"
            "   - Phone: 1-866-442-2529 | Website: https://www.calbar.ca.gov\n\n"
            "🆘 **If you are in immediate danger:** Call 911 or the National DV Hotline: 1-800-799-7233"
        )
