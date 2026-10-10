"""
agents/legal_research.py
------------------------
Agent 2: Legal Research Agent
------------------------------
Responsibility: Research applicable laws, statutes, regulations, and rights
relevant to the user's jurisdiction and legal issue. Provide official source
references wherever possible.

Uses the structured output from Agent 1 (Query Understanding) as context.
"""

from utils.granite_client import call_granite

SYSTEM_PROMPT = """You are a specialised Legal Research Agent powered by IBM Granite.
Your ONLY role is to research and summarise relevant laws, statutes, regulations, 
and legal rights applicable to a given jurisdiction and legal issue.

Rules you must follow:
1. Research laws ONLY for the specified jurisdiction (country and state/province).
2. Cite actual law names, codes, and section numbers where possible.
3. Provide official government/court website URLs as source references.
4. Cover: applicable statutes, key rights, legal procedures, and timelines.
5. Never provide personalised legal advice — present general legal information only.
6. If the law differs significantly between jurisdictions, note this clearly.
7. Be thorough but concise — use bullet points and numbered lists.
8. Flag any recent changes to laws that may be relevant.
9. Always recommend verifying information with current official sources.
10. Use plain, accessible language alongside any technical legal terms."""


def run(query_analysis: str, country: str, state: str, issue_category: str) -> str:
    """
    Execute the Legal Research Agent.

    Parameters
    ----------
    query_analysis : Structured output from Agent 1 (Query Understanding)
    country        : User's country
    state          : User's state / province / region
    issue_category : Selected legal issue category

    Returns
    -------
    str : Legal research summary with citations and sources
    """
    jurisdiction = f"{state}, {country}" if state.strip() else country

    user_prompt = f"""Based on the following legal query analysis, research the applicable laws and rights:

JURISDICTION: {jurisdiction}
LEGAL ISSUE CATEGORY: {issue_category}

QUERY ANALYSIS FROM AGENT 1:
{query_analysis}

Please provide comprehensive legal research including:

1. **Applicable Laws & Statutes**: List relevant laws with their official names and section numbers
2. **Key Legal Rights**: What rights does the person have in this jurisdiction?
3. **Legal Procedures**: What is the standard legal process for this type of issue?
4. **Important Timelines**: Are there deadlines, limitation periods, or time-sensitive requirements?
5. **Recent Legal Changes**: Note any significant recent changes to relevant laws
6. **Official Sources**: Provide URLs to official government/court websites for verification
7. **Jurisdiction-Specific Notes**: Any important variations specific to {jurisdiction}?

Provide factual legal information only — not legal advice. Always encourage consultation with a qualified lawyer."""

    return call_granite(prompt=user_prompt, system_prompt=SYSTEM_PROMPT)
