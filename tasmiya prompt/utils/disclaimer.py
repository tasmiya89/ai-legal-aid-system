"""
utils/disclaimer.py
-------------------
Legal disclaimer text for the AI Legal Aid Multi-Agent System.
This disclaimer is injected into EVERY API response — no exceptions.
This is a core ethical and legal safeguard.
"""

LEGAL_DISCLAIMER = """
⚠️ IMPORTANT LEGAL DISCLAIMER

This AI Legal Aid System provides **general legal information only** — not legal advice.

• The information generated is for educational purposes and does not constitute legal advice.
• This system does **not** replace a qualified, licensed lawyer or legal professional.
• Laws change frequently; always verify information with current official sources.
• Results are AI-generated and may contain errors or omissions.
• Your specific situation may have important facts that change the legal outcome.
• Do not rely solely on this information to make legal decisions.

**Always consult a qualified lawyer before taking legal action.**

If you are in immediate danger or facing a legal emergency, contact local emergency services (911 in the US) or a crisis helpline immediately.
""".strip()

CRISIS_RESOURCES = """
🆘 CRISIS & EMERGENCY RESOURCES

If you are in immediate danger:
• Emergency Services: 911 (US) | 999 (UK) | 112 (EU) | 000 (Australia)
• National Domestic Violence Hotline (US): 1-800-799-7233 | thehotline.org
• National Sexual Assault Hotline (US): 1-800-656-4673 | rainn.org
• Crisis Text Line (US/UK/CA): Text HOME to 741741
• Childhelp National Child Abuse Hotline: 1-800-422-4453
• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

Please reach out to a trusted person, emergency services, or a crisis organisation immediately.
""".strip()

SHORT_DISCLAIMER = (
    "ℹ️ AI-generated legal information only — not legal advice. "
    "Always consult a qualified lawyer for your specific situation."
)
