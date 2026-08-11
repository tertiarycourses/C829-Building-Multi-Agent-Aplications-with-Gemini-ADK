<div align="center">

# Building Multi Agent Aplications with Gemini ADK

[![Course](https://img.shields.io/badge/Course-C829-1f6feb?style=for-the-badge)](https://www.tertiarycourses.com.sg/building-multi-agent-aplications-with-gemini-adk.html)
[![Google ADK](https://img.shields.io/badge/Google_ADK-2.5.0-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://adk.dev/)
[![Gemini](https://img.shields.io/badge/Gemini-3.6_Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/gemini-api/docs/models)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-fbbf24?style=for-the-badge)](#license)

**Hands-on courseware and connected labs for designing, building, testing, and preparing production-grade multi-agent applications with Google Agent Development Kit and Gemini.**

[Course Page](https://www.tertiarycourses.com.sg/building-multi-agent-aplications-with-gemini-adk.html) · [Learner Guide](LEARNER-GUIDE.md) · [Labs](labs/README.md) · [Report a Bug](https://github.com/tertiarycourses/C829-Building-Multi-Agent-Aplications-with-Gemini-ADK/issues)

</div>

> [!NOTE]
> These are the official learning materials for **Building Multi Agent Aplications with Gemini ADK**.  
> **Course Code:** `C829` · Tertiary Courses / Tertiary Infotech

---

## About

This repository contains the slide deck, Learner Guide, Lesson Plan, and eight connected hands-on labs for course C829. Learners progressively build **SupportOps**, a multi-agent service-operations assistant that can classify requests, use tools, retain session context, route work to specialists, connect to an MCP server, and apply production guardrails.

The implementation targets **Google ADK 2.5.0** and the stable **Gemini 3.6 Flash** model. Course examples use synthetic support tickets and placeholder secrets only.

### What You Will Learn

| Topic | Focus | Working outcome |
|---|---|---|
| **1. Single Agent Foundations** | Agent lifecycle, model instructions, structured output, sessions | A runnable ticket-triage agent with typed JSON output |
| **2. Tools, Memory and Sessions** | Function tools, API integration, error handling, state, searchable memory | A stateful support agent grounded in a local knowledge base |
| **3. Multi-Agent Architecture** | Specialisation, coordinator routing, delegation, graph workflows | A coordinator with billing, technical, and account specialists |
| **4. MCP and Production Design** | MCP discovery, routing, observability, security, deployment | An MCP-enabled, traced, guarded application ready for container deployment |

---

## Lab Activities

| # | Lab | You build |
|---|---|---|
| **1** | Create the SupportOps Agent | A minimal ADK project running in the development web UI |
| **2** | Add Structured Triage and Sessions | Typed ticket classification with per-user session state |
| **3** | Connect Reliable Function Tools | Ticket lookup and update tools with validation and recoverable errors |
| **4** | Add Searchable Knowledge and Memory | Local semantic retrieval plus cross-turn user preferences |
| **5** | Build a Specialist Agent Team | Billing, technical, and account agents behind a coordinator |
| **6** | Orchestrate a Deterministic Resolution Pipeline | An ADK graph workflow with explicit routing and hand-offs |
| **7** | Discover Tools Through MCP | A local MCP server connected through `McpToolset` |
| **8** | Harden, Observe, and Package SupportOps | Guardrails, structured logging, tests, and a production container |

The labs are designed as one continuous build. Each lab ends with a checkpoint that the next lab can use.

---

## Architecture

```text
User request
    |
    v
SupportOps coordinator
    |-- billing specialist ------ ticket and refund tools
    |-- technical specialist ---- knowledge search and diagnostics
    `-- account specialist ------ customer profile tools
             |
             v
      shared session state
             |
             v
MCP tool discovery -> policy guardrails -> traces and logs -> deployment
```

---

## Repository Structure

```text
C829-Building-Multi-Agent-Aplications-with-Gemini-ADK/
|-- README.md
|-- LEARNER-GUIDE.md
|-- courseware/
|   |-- Building Multi Agent Aplications with Gemini ADK (C829)-v1.0.pptx
|   |-- Building Multi Agent Aplications with Gemini ADK (C829)-v1.0.pdf
|   |-- LG-Building Multi Agent Aplications with Gemini ADK (C829).docx
|   `-- LP-Building Multi Agent Aplications with Gemini ADK (C829).docx
|-- labs/
|   |-- README.md
|   `-- lab-01-...md through lab-08-...md
|-- starter/
|   |-- support_ops/
|   |-- tests/
|   |-- requirements.txt
|   `-- Dockerfile
`-- .agents/skills/non-wsq-courseware-build/
    `-- build/                  # single-source courseware generator
```

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- A Google AI Studio API key stored as `GOOGLE_API_KEY`
- Git and a modern web browser
- Docker Desktop for the final packaging lab

### 1. Clone the repository

```bash
git clone https://github.com/tertiarycourses/C829-Building-Multi-Agent-Aplications-with-Gemini-ADK.git
cd C829-Building-Multi-Agent-Aplications-with-Gemini-ADK
```

### 2. Create an isolated environment

```bash
cd starter
python -m venv .venv
```

Activate it with `.venv\\Scripts\\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Gemini safely

Copy `.env.example` to `.env` and replace the placeholder locally. Never commit `.env` or paste a real key into source code, prompts, screenshots, or lab submissions.

### 4. Run the agent

```bash
adk web .
```

Open the URL shown by ADK, select `support_ops`, and follow [Lab 1](labs/lab-01-create-the-supportops-agent.md).

---

## Courseware

All learner-facing artifacts are generated from one content source so the topic order, learning outcomes, lab titles, lab numbers, and schedule stay aligned. The generated PPT/PDF, Learner Guide, and Lesson Plan are in [`courseware/`](courseware/); full executable lab instructions are in [`labs/`](labs/).

---

## Contributing

Corrections and improvements are welcome. Create a focused branch, include a reproducible test or verification note, and open a pull request. Do not commit API keys, customer data, `.env` files, or generated virtual environments.

---

## License

This material is provided for educational use as part of course **C829**. © Tertiary Infotech Academy Pte Ltd. All rights reserved.

---

## Developed By

**Tertiary Infotech Academy Pte Ltd** · [Tertiary Courses](https://www.tertiarycourses.com.sg/)  
Course: [Building Multi Agent Aplications with Gemini ADK (C829)](https://www.tertiarycourses.com.sg/building-multi-agent-aplications-with-gemini-adk.html)

## Acknowledgements

- [Google Agent Development Kit](https://adk.dev/) — agent and workflow framework
- [Google Gemini](https://ai.google.dev/gemini-api/docs/models) — language model family
- [Model Context Protocol](https://modelcontextprotocol.io/) — interoperable tool and context protocol

---

<div align="center">

Powered by [Tertiary Infotech Academy Pte Ltd](https://www.tertiaryinfotech.com/)

[Course Page](https://www.tertiarycourses.com.sg/building-multi-agent-aplications-with-gemini-adk.html) · [Learner Guide](LEARNER-GUIDE.md) · [Labs](labs/README.md)

</div>
