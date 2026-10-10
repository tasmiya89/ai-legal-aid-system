"""
agents/document_analysis.py
----------------------------
Agent 3: Document Analysis & Plain-Language Explanation Agent
--------------------------------------------------------------
Responsibility: Take the legal research results and translate them into
clear, accessible, plain-English explanations that a non-lawyer can
understand and act upon. Provide practical next steps.

Uses output from both Agent 1 and Agent 2 as context.
"""

from utils.granite_client import call_granite

SYSTEM_PROMPT = """You are a specialised Legal Document Analysis and Plain-Language Explanation Agent 
powered by IBM Granite.

Your role is to translate complex legal information into clear, accessible plain English 
that anyone — regardless of their legal knowledge — can understand and use.

Rules you must follow:
1. Translate legal jargon into everyday language.
2. Use clear, empathetic, and respectful language.
3. Structure information with clear headings and short paragraphs.
4. Provide practical, actionable next steps the person can take.
5. Highlight the most important points prominently.
6. Never minimise the seriousness of someone's legal situation.
7. Always acknowledge emotional difficulty where relevant (e.g., family law, eviction).
8. Use ✅ for positive rights/options and ⚠️ for warnings/time-sensitive items.
9. Never provide specific legal advice — explain what the law generally says.
10. End with a clear recommendation to consult a qualified lawyer."""


def run(query_analysis: str, legal_research: str, country: str, state: str, issue_category: str) -> str:
    """
    Execute the Document Analysis Agent.

    Parameters
    ----------
    query_analysis  : Output from Agent 1
    legal_research  : Output from Agent 2
    country         : User's country
    state           : User's state / province
    issue_category  : Legal issue category

    Returns
    -------
    str : Plain-language explanation with practical next steps
    """
    jurisdiction = f"{state}, {country}" if state.strip() else country

    user_prompt = f"""Using the legal research below, create a clear, plain-English explanation 
for someone dealing with a {issue_category} issue in {jurisdiction}.

QUERY ANALYSIS:
{query_analysis}

LEGAL RESEARCH:
{legal_research}

Please provide:

1. **What This Means For You** (plain-language summary — avoid all jargon)
2. **Your Key Rights** (bullet points — simple and clear)
3. **What Your Situation Likely Involves** (explain the process in plain English)
4. **Important Warnings** (use ⚠️ for anything time-sensitive or critical)
5. **Practical Next Steps** (numbered list — what should the person do first, second, third?)
6. **What to Expect** (what is the typical timeline and process?)
7. **When to Act Urgently** (are there any deadlines they must meet immediately?)

Write as if explaining to a friend who has no legal knowledge. Be warm, clear, and supportive.
Remind them at the end that this is general information and they should speak to a lawyer."""

    return call_granite(prompt=user_prompt, system_prompt=SYSTEM_PROMPT)
