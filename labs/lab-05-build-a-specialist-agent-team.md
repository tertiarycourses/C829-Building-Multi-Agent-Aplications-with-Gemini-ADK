# Lab 5 — Build a Specialist Agent Team

**Course:** Building Multi Agent Aplications with Gemini ADK (C829)<br>
**Topic 3:** Multi-Agent Architecture<br>
**Maps to:** LO4: Design a coordinator with bounded billing, technical, and account specialists using clear delegation contracts.<br>
**Tools:** Google ADK collaborative agents, Gemini 3.6 Flash, specialist tools, ADK trace inspector

**Version:** v1.0 (11 August 2026)<br>
**Duration:** 65 minutes

---

## Goal

You split SupportOps into three least-privilege specialists and place them behind one coordinator. Each specialist has a narrow description, instruction, mode, and tool set; the coordinator owns user communication and delegation. You test obvious, ambiguous, and out-of-scope requests to see how model-driven routing behaves and where descriptions become part of the architecture.

## What You Will Build

A collaborative ADK agent team whose coordinator delegates synthetic requests to billing, technical, or account specialists.

## Prerequisites

- Complete the Day 1 checkpoint through Lab 4.
- Retain work/support_ops/tools.py and knowledge.py; start the local ticket API only for ticket lookup prompts.
- Review the allowed responsibility and tool boundary for each specialist before coding.

> **Data note.** Use only the synthetic ticket, customer, and knowledge data supplied in this repository. Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git.

## Steps

**1. Create work/support_ops/team.py with three specialists. mode=single_turn prevents a specialist from taking over the whole conversation and supports bounded return to the coordinator.**

```text
import os
from dotenv import load_dotenv
from google.adk import Agent
from .knowledge import search_knowledge
from .tools import get_ticket

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

billing_agent = Agent(
    name="billing_specialist",
    model=MODEL,
    mode="single_turn",
    description="Handles duplicate charges, invoices, payment evidence, and other synthetic billing questions.",
    instruction=(
        "Handle only billing work. Retrieve a synthetic ticket when an ID is present and search the runbook for procedure. "
        "Return facts, source IDs, missing evidence, and a recommended next step to the coordinator. Do not promise refunds."
    ),
    tools=[get_ticket, search_knowledge],
)

technical_agent = Agent(
    name="technical_specialist",
    model=MODEL,
    mode="single_turn",
    description="Handles login failures, API timeouts, diagnostics, and synthetic technical runbook questions.",
    instruction=(
        "Handle only technical diagnosis. Search the runbook, cite source IDs, separate observed facts from hypotheses, "
        "and return a bounded diagnostic next step. Do not change tickets or accounts."
    ),
    tools=[search_knowledge],
)

account_agent = Agent(
    name="account_specialist",
    model=MODEL,
    mode="single_turn",
    description="Handles account access, suspected takeover, and identity-protection guidance for synthetic users.",
    instruction=(
        "Handle only account access and security guidance. Search the runbook and prioritise containment. "
        "Do not change contact details, reveal secrets, or perform account actions. Return safe next steps and source IDs."
    ),
    tools=[search_knowledge],
)

root_agent = Agent(
    name="support_ops_coordinator",
    model=MODEL,
    description="Coordinates specialist help for synthetic service requests.",
    instruction=(
        "Clarify the user's goal, delegate domain work to exactly the relevant specialist, then present one coherent answer. "
        "Do not perform specialist work yourself. If the request spans domains, state the order and delegate one bounded task at a time. "
        "If no specialist owns the request, explain the boundary instead of inventing a route."
    ),
    sub_agents=[billing_agent, technical_agent, account_agent],
)
```

**2. Replace work/support_ops/agent.py with the package entry point. ADK still discovers one root_agent even though the implementation now contains four agents.**

```text
from .team import root_agent
```

**3. Create work/tests/test_team.py. These tests verify ownership and least-privilege tool allocation without calling Gemini.**

```text
from support_ops.team import account_agent, billing_agent, root_agent, technical_agent

def _tool_names(agent):
    return {getattr(tool, "name", getattr(tool, "__name__", type(tool).__name__)) for tool in agent.tools}

def test_coordinator_has_three_distinct_specialists():
    assert {agent.name for agent in root_agent.sub_agents} == {
        "billing_specialist", "technical_specialist", "account_specialist"
    }

def test_only_billing_can_read_ticket_records():
    assert "get_ticket" in _tool_names(billing_agent)
    assert "get_ticket" not in _tool_names(technical_agent)
    assert "get_ticket" not in _tool_names(account_agent)

def test_all_specialists_are_bounded_single_turn_workers():
    assert all(agent.mode == "single_turn" for agent in root_agent.sub_agents)
```

**4. Run the team contract tests and the full Day 1 regression suite from the repository root, with work/ as pytest's working directory.**

```text
python -c "import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd='work').returncode)"
```

**5. If you will test TKT-1001, start the local API from the repository root in terminal 1. Otherwise the knowledge-only prompts do not need it.**

```text
python -m uvicorn --app-dir work support_ops.mock_api:app --host 127.0.0.1 --port 8765
```

**6. Start ADK Web with the work/ agents directory in terminal 2 and select support_ops.**

```text
adk web work
```

**7. Send an obvious billing request. In the trace, identify the coordinator decision, billing_specialist invocation, tool calls, specialist return, and coordinator response.**

```text
For synthetic ticket TKT-1001, what duplicate-charge evidence should I collect?
```

**8. Send an obvious technical request. Confirm the technical specialist can search knowledge but cannot retrieve or mutate tickets.**

```text
Our idempotent API request timed out. What diagnostic evidence should I record before retrying?
```

**9. Send an account-security request. Confirm the account specialist prioritises containment and cites RB-SEC-04.**

```text
A synthetic user reports a suspected account takeover. What should happen first?
```

**10. Test an ambiguous request and observe whether the coordinator asks a question or chooses a route. Improve one specialist description if the route is not defensible.**

```text
The customer says access stopped after a payment problem. Help.
```

**11. Test an out-of-scope request. The coordinator should state the boundary instead of delegating to the least-wrong specialist.**

```text
Book a courier to collect a laptop tomorrow.
```

**12. Save the checkpoint and write down one routing failure mode you observed.**

```text
python -c "from pathlib import Path; Path('work/CHECKPOINT-LAB-05.txt').write_text('Coordinator delegation and specialist boundaries verified\n', encoding='utf-8')"
```

## Test It

From the repository root, the portable pytest command must pass. In ADK Web, the three obvious prompts must delegate to billing_specialist, technical_specialist, and account_specialist respectively. The technical and account traces must not contain get_ticket. The out-of-scope prompt must not be forced into an unrelated specialist.

## Troubleshooting

- **Every request stays with the coordinator.** Make each specialist description distinct and capability-focused, restart ADK Web, and confirm root_agent.sub_agents contains all three objects.
- **The wrong specialist is selected.** Remove overlapping phrases from descriptions and add a coordinator example or clarification rule for the ambiguous boundary.
- **A specialist does not return control.** Confirm mode is exactly single_turn and that the specialist instruction asks for a bounded result to the coordinator.

## Challenge

Add a general_support specialist with no tools that only asks clarifying questions, then test whether it reduces forced routing without stealing clear domain requests.

## Reflection

What concrete benefit did each agent boundary provide—different tools, different policy, different evaluation, or only a different name?

---

[← Lab 4](lab-04-add-searchable-knowledge-and-memory.md) · [Lab 6 →](lab-06-orchestrate-a-deterministic-resolution-pipeline.md)
