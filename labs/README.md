# Building Multi Agent Aplications with Gemini ADK (C829) — Hands-On Labs

8 labs across 4 topics · 2 days · 15 scheduled hours

Work through the labs in order — each one builds on the artifacts you produced in the labs before it.


## Topic 1 — Single Agent Foundations

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 1 | [Create the SupportOps Agent](lab-01-create-the-supportops-agent.md) | Python 3.10+, Google ADK 2.5.0, Gemini 3.6 Flash, ADK Web | A clean work/ project containing a discoverable support_ops.root_agent and a captured first-turn event trace. |
| 2 | [Add Structured Triage and Sessions](lab-02-add-structured-triage-and-sessions.md) | Google ADK, Pydantic, ADK Web session and event inspector, pytest | A typed TicketTriage response with category, urgency, summary, and next_action stored as latest_triage in the active session. |

## Topic 2 — Tools, Memory and Sessions

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 3 | [Connect Reliable Function Tools](lab-03-connect-reliable-function-tools.md) | Google ADK Function Tools, FastAPI, Uvicorn, HTTPX, pytest | A tool-enabled SupportOps agent that can retrieve a synthetic ticket and safely change its priority through a local HTTP API. |
| 4 | [Add Searchable Knowledge and Memory](lab-04-add-searchable-knowledge-and-memory.md) | Chroma 1.5.9, Google ADK ToolContext, session state, pytest | A SupportOps agent with semantic runbook retrieval, source identifiers, and a user-scoped response-style preference. |

## Topic 3 — Multi-Agent Architecture

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 5 | [Build a Specialist Agent Team](lab-05-build-a-specialist-agent-team.md) | Google ADK collaborative agents, Gemini 3.6 Flash, specialist tools, ADK trace inspector | A collaborative ADK agent team whose coordinator delegates synthetic requests to billing, technical, or account specialists. |
| 6 | [Orchestrate a Deterministic Resolution Pipeline](lab-06-orchestrate-a-deterministic-resolution-pipeline.md) | Google ADK 2.x Workflow, Event routing, Pydantic schemas, Gemini specialist nodes, pytest | A SupportOps Workflow with explicit START → triage → route → specialist edges for billing, technical, account, and general requests. |

## Topic 4 — MCP and Production Design

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 7 | [Discover Tools Through MCP](lab-07-discover-tools-through-mcp.md) | Model Context Protocol Python SDK, FastMCP, ADK McpToolset, stdio transport, ADK trace inspector | A local SupportOps MCP server plus an ADK client agent that discovers and calls only lookup_runbook. |
| 8 | [Harden, Observe, and Package SupportOps](lab-08-harden-observe-and-package-supportops.md) | ADK callbacks, Python logging, pytest, ADK API server, Docker, OpenTelemetry-ready configuration | A production-oriented multi-agent SupportOps supervisor with the specialist hierarchy, tested policy callbacks, bounded MCP access, structured telemetry, executable evaluation cases, and a Docker image definition. |

---

> Use only the synthetic ticket, customer, and knowledge data supplied in this repository. Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git.


_Tertiary Infotech Academy Pte Ltd · C829 · v1.0 (11 August 2026)_
