"""
agents/query_understanding.py
-----------------------------
Agent 1: Query Understanding Agent
-----------------------------------
Responsibility: Parse the user's legal issue, extract jurisdiction details,
identify the core legal question, assess urgency, and structure the query
for downstream agents.

IBM Granite is used with a carefully crafted system prompt that keeps this
agent strictly within legal information territory.
"""

from utils.granite_client import call_granite

SYSTEM_PROMPT = """You are a specialised Legal Query Understanding Agent powered by IBM Granite.
Your ONLY role is to analyse a user's legal query and produce a structured classification.

Rules you must follow:
1. Focus exclusively on legal matters — do not engage with off-topic requests.
2. Never provide specific legal advice — your role is classification and understanding only.
3. Identify the jurisdiction (country and state/province if given).
4. Extract the core legal question(s) from the user's description.
5. Identify key legal concepts, rights, or procedures that may be relevant.
6. Assess urgency level: Low / Medium / High / Critical.
7. Flag if crisis resources should be shown (domestic violence, immediate danger, etc.).
8. Be respectful, clear, and use plain language.
9. Structure your output with clear headings and bullet points.
10. Always acknowledge that this is informational only."""


def run(country: str, state: str, issue_category: str, description: str) -> str:
    """
    Execute the Query Understanding Agent.

    Parameters
    ----------
    country        : User's country
    state          : User's state / province / region
    issue_category : Selected legal issue category
    description    : User's free-text description of their problem

    Returns
    -------
    str : Structured analysis of the legal query
    """
    jurisdiction = f"{state}, {country}" if state.strip() else country

    user_prompt = f"""Please analyse the following legal query and provide a structured understanding:

JURISDICTION: {jurisdiction}
LEGAL ISSUE CATEGORY: {issue_category}
USER'S DESCRIPTION: {description if description.strip() else "(No additional description provided — use issue category only)"}

Please provide:
1. **Issue Classification**: What type of legal matter is this?
2. **Jurisdiction Notes**: What jurisdiction-specific context is relevant?
3. **Core Legal Question(s)**: What is the user fundamentally asking?
4. **Key Legal Concepts**: What legal terms, rights, or procedures are likely involved?
5. **Urgency Assessment**: Is this Low / Medium / High / Critical urgency? Why?
6. **Recommended Research Areas**: What laws, statutes, or rights should be researched?

Remember: Provide analysis and classification only — no legal advice."""

    return call_granite(prompt=user_prompt, system_prompt=SYSTEM_PROMPT)
