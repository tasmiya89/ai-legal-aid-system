# AI Legal Aid Multi-Agent System — Project Plan

**Powered by IBM Granite LLM | Agentic AI SDLC**

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Phase 1 — Planning](#2-phase-1--planning)
3. [Phase 2 — Design](#3-phase-2--design)
4. [Phase 3 — Development](#4-phase-3--development)
5. [Phase 4 — Testing](#5-phase-4--testing)
6. [Phase 5 — Deployment](#6-phase-5--deployment)
7. [Phase 6 — Maintenance](#7-phase-6--maintenance)
8. [AI Ethics & Guardrails](#8-ai-ethics--guardrails)
9. [Technology Stack](#9-technology-stack)
10. [Directory Structure](#10-directory-structure)

---

## 1. Project Overview

The **AI Legal Aid Multi-Agent System** is a web-based application that provides accessible, 
personalized legal information to users using IBM Granite LLM as the AI backbone. It employs 
a pipeline of specialized AI agents to understand legal queries, research applicable laws, 
analyze legal documents, and locate legal aid resources.

### Goals
- Make legal information accessible to all, regardless of financial ability
- Provide jurisdiction-specific (country + state) legal guidance
- Leverage IBM Granite's responsible AI capabilities
- Maintain strict ethical guardrails and privacy protection
- Always recommend professional legal counsel

### Constraints & Boundaries
- The system provides **information only**, not legal advice
- Output is not a substitute for a qualified lawyer
- No personally identifiable information (PII) is stored
- All responses include a mandatory legal disclaimer

---

## 2. Phase 1 — Planning

### 2.1 Stakeholder Analysis
| Stakeholder        | Need                                                        |
|--------------------|-------------------------------------------------------------|
| End Users          | Clear, simple legal information in plain language           |
| Legal Aid Orgs     | Automated first-response to reduce caseload                 |
| Developers         | Clean architecture, maintainable codebase                   |
| Regulatory Bodies  | Compliance, ethics, and data privacy adherence              |

### 2.2 Requirements

#### Functional Requirements
- FR-01: Collect user's country, state, legal issue category, and problem description
- FR-02: Route queries through a 4-agent pipeline
- FR-03: Agent 1 — Query Understanding Agent: parse and classify legal query
- FR-04: Agent 2 — Legal Research Agent: research relevant laws and statutes
- FR-05: Agent 3 — Document Analysis Agent: analyze and summarize legal context
- FR-06: Agent 4 — Legal Aid Finder Agent: locate free/low-cost legal aid resources
- FR-07: Generate a consolidated legal information report
- FR-08: Display official source references
- FR-09: Provide a legal disclaimer on every response
- FR-10: Support multiple legal issue categories (criminal, civil, family, employment, housing, immigration, consumer)

#### Non-Functional Requirements
- NFR-01: Response time < 30 seconds for full pipeline
- NFR-02: Graceful degradation if IBM watsonx API is unavailable
- NFR-03: No PII stored in logs or databases
- NFR-04: HTTPS-ready configuration
- NFR-05: Accessible UI (WCAG 2.1 AA)

### 2.3 Risk Register
| Risk                          | Likelihood | Impact | Mitigation                              |
|-------------------------------|------------|--------|-----------------------------------------|
| IBM watsonx API unavailability| Low        | High   | Fallback static responses               |
| Inaccurate legal information  | Medium     | High   | Disclaimer + source citations           |
| PII leakage via prompts       | Medium     | High   | Input sanitization + no logging of PII  |
| User over-reliance on AI      | High       | Medium | Prominent disclaimer + lawyer referrals |
| Rate limiting on API          | Medium     | Medium | Response caching + retry logic          |

---

## 3. Phase 2 — Design

### 3.1 Multi-Agent Architecture

```
User Input (Country, State, Issue, Description)
        │
        ▼
┌─────────────────────────────────┐
│   Agent 1: Query Understanding  │  ← Classify, extract intent, identify jurisdiction
│   (IBM Granite LLM)             │
└──────────────┬──────────────────┘
               │ Structured Query Context
               ▼
┌─────────────────────────────────┐
│   Agent 2: Legal Research       │  ← Research laws, statutes, rights, procedures
│   (IBM Granite LLM)             │
└──────────────┬──────────────────┘
               │ Legal Research Summary
               ▼
┌─────────────────────────────────┐
│   Agent 3: Document Analysis    │  ← Analyze legal language, explain in plain English
│   (IBM Granite LLM)             │
└──────────────┬──────────────────┘
               │ Plain-language Analysis
               ▼
┌─────────────────────────────────┐
│   Agent 4: Legal Aid Finder     │  ← Locate free/low-cost legal resources & contacts
│   (IBM Granite LLM)             │
└──────────────┬──────────────────┘
               │
               ▼
       Consolidated Legal Report
       (with disclaimer + sources)
```

### 3.2 Data Flow
1. User submits form → Flask API `/api/legal-query`
2. Input sanitized and validated
3. Agent pipeline executed sequentially
4. Each agent receives prior agent's output as context
5. Final report assembled and returned as JSON
6. Frontend renders structured report with disclaimer

### 3.3 UI Design Principles
- Clean, professional, trustworthy aesthetic
- Clear progress indicator during agent pipeline execution
- Expandable sections for each agent's output
- Prominent legal disclaimer at top and bottom of results
- Mobile-responsive design
- Accessibility: ARIA labels, keyboard navigation, sufficient color contrast

---

## 4. Phase 3 — Development

### 4.1 Project Structure
```
legal-aid-system/
├── app.py                  # Flask application entry point
├── agents/
│   ├── __init__.py
│   ├── query_understanding.py   # Agent 1
│   ├── legal_research.py        # Agent 2
│   ├── document_analysis.py     # Agent 3
│   └── legal_aid_finder.py      # Agent 4
├── config/
│   ├── __init__.py
│   └── settings.py              # IBM Granite & app config
├── utils/
│   ├── __init__.py
│   ├── sanitizer.py             # Input sanitization & guardrails
│   ├── disclaimer.py            # Legal disclaimer text
│   └── granite_client.py        # IBM watsonx.ai client wrapper
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── requirements.txt
├── .env.example
├── run_project.bat
└── PROJECT_PLAN.md
```

### 4.2 IBM Granite Model
- **Model ID**: `ibm/granite-3-3-8b-instruct`
- **Platform**: IBM watsonx.ai (ibm-watsonx-ai SDK)
- **Parameters**: temperature=0.3 (for reliable, factual outputs), max_new_tokens=800

### 4.3 Agent Prompting Strategy
Each agent uses a structured system prompt + dynamic user prompt:
- System prompt defines the agent's role, jurisdiction awareness, and ethics constraints
- User prompt injects context from previous agents
- Output is structured JSON or Markdown parsed by the pipeline

---

## 5. Phase 4 — Testing

### 5.1 Test Cases
| Test ID | Description                                      | Expected Outcome                              |
|---------|--------------------------------------------------|-----------------------------------------------|
| T-01    | Submit a tenant rights query (US, California)    | Relevant CA tenant law information returned   |
| T-02    | Submit employment discrimination query (UK)      | UK Equality Act references returned           |
| T-03    | Empty description field                          | System uses issue category only               |
| T-04    | Injection attempt in description                 | Sanitized; no prompt injection                |
| T-05    | API key missing/invalid                          | Graceful error message shown                  |
| T-06    | Legal disclaimer presence                        | Disclaimer present on all responses           |
| T-07    | Legal aid resources returned                     | At least one resource URL/organization listed |
| T-08    | Mobile responsiveness                            | UI renders correctly on 375px viewport        |

### 5.2 Guardrail Tests
- Attempt to elicit specific legal advice → agent redirects to general information
- Attempt to collect PII → system strips and does not store
- Attempt to generate content outside legal domain → agent declines gracefully

---

## 6. Phase 5 — Deployment

### 6.1 Local Deployment (Windows)
1. Run `run_project.bat` to install dependencies and start the server
2. Open browser at `http://localhost:5000`

### 6.2 Production Deployment Options
- **IBM Cloud Code Engine**: Container-based serverless deployment
- **Docker**: `Dockerfile` can be added for containerization
- **Environment Variables**: All secrets via `.env` file (never hardcoded)

### 6.3 Environment Variables Required
```
WATSONX_API_KEY=your_ibm_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=your_secret_key
```

---

## 7. Phase 6 — Maintenance

### 7.1 Ongoing Tasks
- Monitor IBM Granite model updates and migrate to newer versions
- Review legal information accuracy quarterly with legal domain experts
- Update legal aid resource databases periodically
- Monitor API usage and costs
- Review and update ethical guardrails as AI regulations evolve

### 7.2 Versioning
- Semantic versioning: MAJOR.MINOR.PATCH
- Current version: **1.0.0**

---

## 8. AI Ethics & Guardrails

### 8.1 Core Ethical Principles
| Principle         | Implementation                                                      |
|-------------------|---------------------------------------------------------------------|
| Transparency      | All AI-generated content is labeled; sources cited                  |
| Fairness          | Jurisdiction-specific responses; no demographic bias in prompts     |
| Privacy           | No PII stored; inputs not logged; session-based only                |
| Accountability    | Legal disclaimer on every response; always recommend a lawyer       |
| Non-maleficence   | Guardrails prevent harmful legal advice; crisis resources included  |
| Reliability       | IBM Granite low-temperature settings for factual, consistent output |

### 8.2 Guardrail Implementation
- **Input Sanitization**: Remove HTML, scripts, and prompt injection patterns
- **Topic Guardrails**: Agents restricted to legal information domain
- **Output Validation**: Responses checked for harmful content patterns
- **Mandatory Disclaimer**: Injected into every API response regardless of content
- **Crisis Detection**: If domestic violence, criminal emergency keywords detected → crisis resources shown immediately

### 8.3 Privacy Protection
- No database storage of user queries
- No session data persisted beyond request lifecycle
- No third-party analytics
- IP addresses not logged
- `.env` for all credentials (never committed to version control)

---

## 9. Technology Stack

| Layer           | Technology                                      |
|-----------------|-------------------------------------------------|
| AI Engine       | IBM Granite 3.3 8B Instruct (ibm-watsonx-ai)   |
| Backend         | Python 3.9+ / Flask 3.x                        |
| Frontend        | HTML5 / CSS3 / Vanilla JavaScript               |
| HTTP Client     | ibm-watsonx-ai SDK                             |
| Environment     | python-dotenv                                   |
| Input Safety    | bleach, re (Python standard library)            |
| Deployment      | Windows (run_project.bat) / Cross-platform      |

---

## 10. Directory Structure

See Section 4.1 for full directory layout.

---

*Document version: 1.0.0 | Last updated: 2025*  
*This system is built in compliance with IBM's AI Ethics principles and responsible AI guidelines.*
