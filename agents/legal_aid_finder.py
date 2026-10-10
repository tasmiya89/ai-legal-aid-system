"""
agents/legal_aid_finder.py
--------------------------
Agent 4: Legal Aid Resource Finder Agent
-----------------------------------------
Responsibility: Identify free and low-cost legal aid organisations,
government legal services, court self-help resources, and lawyer
referral services relevant to the user's jurisdiction and legal issue.

This agent helps bridge the justice gap by connecting people with
accessible legal assistance.
"""

from utils.granite_client import call_granite

SYSTEM_PROMPT = """You are a specialised Legal Aid Resource Finder Agent powered by IBM Granite.
Your role is to help people find FREE and low-cost legal assistance, government legal services, 
court self-help resources, and lawyer referral programs.

You exist because access to justice is a fundamental right, and many people cannot 
afford a private lawyer. Your job is to connect them with help.

Rules you must follow:
1. Focus on FREE and LOW-COST resources first — prioritise accessibility.
2. Include government legal aid programs (they are most reliable).
3. Include court self-help centres where available.
4. Include law school legal clinics (often free).
5. Include bar association lawyer referral services.
6. Include relevant non-profit legal organisations.
7. Provide website URLs and phone numbers where you can.
8. Organise resources by type and accessibility.
9. Include online resources (legal information websites, form generators).
10. Always include a note about the state/local bar association as a starting point.
11. If the issue involves domestic violence, include DV-specific legal resources.
12. Be encouraging — finding help is possible even with limited resources."""


def run(query_analysis: str, country: str, state: str, issue_category: str) -> str:
    """
    Execute the Legal Aid Resource Finder Agent.

    Parameters
    ----------
    query_analysis : Output from Agent 1 (provides context on the issue)
    country        : User's country
    state          : User's state / province
    issue_category : Legal issue category

    Returns
    -------
    str : Curated list of legal aid resources with contact details
    """
    jurisdiction = f"{state}, {country}" if state.strip() else country

    user_prompt = f"""Find free and low-cost legal aid resources for someone with a 
{issue_category} legal issue in {jurisdiction}.

CONTEXT FROM QUERY ANALYSIS:
{query_analysis}

Please provide a comprehensive guide to legal aid resources:

1. **Government Legal Aid Programs** 
   - National/federal legal aid programs in {country}
   - State/provincial legal aid offices in {jurisdiction}
   - Eligibility requirements (income, issue type)

2. **Free Court Resources**
   - Court self-help centres
   - Official court forms and guides
   - Links to official court websites

3. **Non-Profit Legal Organisations**
   - Legal aid societies and non-profits serving {jurisdiction}
   - Issue-specific organisations (e.g., tenant rights groups, immigration clinics)

4. **Law School Clinics**
   - Law school legal clinics (typically free)
   - Note which law schools are in {jurisdiction} if known

5. **Online Self-Help Resources**
   - Official legal information websites
   - Court form generators
   - Legal information portals

6. **Lawyer Referral Services**
   - Bar association referral programs
   - Low-cost initial consultation programs

7. **Practical Tips for Getting Help**
   - How to apply for legal aid
   - What documents to bring
   - What to expect when contacting legal aid

For each resource, provide: Name, Website URL, Phone number (if known), and who it serves.
Be encouraging and remind them that help is available."""

    return call_granite(prompt=user_prompt, system_prompt=SYSTEM_PROMPT)
