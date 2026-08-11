# Lab 6 — Orchestrate a Deterministic Resolution Pipeline

**Course:** Building Multi Agent Aplications with Gemini ADK (C829)<br>
**Topic 3:** Multi-Agent Architecture<br>
**Maps to:** LO4, LO5: Build an ADK graph workflow that constrains classification, routing, and specialist execution through typed edges.<br>
**Tools:** Google ADK 2.x Workflow, Event routing, Pydantic schemas, Gemini specialist nodes, pytest

**Version:** v1.0 (11 August 2026)<br>
**Duration:** 55 minutes

---

## Goal

You create a graph-based workflow for requests that must follow an explicit process. A typed triage agent emits one bounded category; a deterministic router converts that value into a graph route; and one single-turn resolver produces the final bounded guidance. You compare this reliable process with the flexible coordinator from Lab 5 and document when each pattern is appropriate.

## What You Will Build

A SupportOps Workflow with explicit START → triage → route → specialist edges for billing, technical, account, and general requests.

## Prerequisites

- Complete Lab 5 and keep team.py as the model-driven delegation example.
- Retain models.py with the TicketTriage schema from Lab 2.
- Understand that graph workflow agents use single-turn nodes and explicit input/output contracts.

> **Data note.** Use only the synthetic ticket, customer, and knowledge data supplied in this repository. Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git.

## Steps

**1. Create work/support_ops/workflow.py. The triage node is model-driven, while route_triage and the edge map are deterministic application logic.**

```text
import os
from dotenv import load_dotenv
from google.adk import Agent, Event, Workflow
from .models import TicketTriage

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

triage_agent = Agent(
    name="triage_node",
    model=MODEL,
    mode="single_turn",
    instruction=(
        "Classify the synthetic request into billing, technical, account, or general. "
        "Return urgency, a factual summary, and one safe next action."
    ),
    output_schema=TicketTriage,
)

def route_triage(record: TicketTriage):
    """Convert the validated category into a deterministic graph route."""
    return Event(route=record.category)

def _resolver(name: str, domain: str) -> Agent:
    return Agent(
        name=name,
        model=MODEL,
        mode="single_turn",
        input_schema=TicketTriage,
        output_schema=str,
        instruction=(
            f"You are the {domain} resolution node. Use only the supplied TicketTriage fields. "
            "Return: Route, Urgency, Known facts, Missing evidence, and Safe next step. "
            "Do not claim to have called a tool or changed a system."
        ),
    )

billing_resolver = _resolver("billing_resolver", "billing")
technical_resolver = _resolver("technical_resolver", "technical")
account_resolver = _resolver("account_resolver", "account")
general_resolver = _resolver("general_resolver", "general support")

root_agent = Workflow(
    name="support_ops_workflow",
    edges=[
        ("START", triage_agent, route_triage),
        (route_triage, {
            "billing": billing_resolver,
            "technical": technical_resolver,
            "account": account_resolver,
            "general": general_resolver,
        }),
    ],
)
```

**2. Replace work/support_ops/agent.py so ADK runs the graph for this checkpoint. team.py remains available for comparison.**

```text
from .workflow import root_agent
```

**3. Create work/tests/test_workflow.py to test the deterministic route function for every allowed category.**

```text
from support_ops.models import TicketTriage
from support_ops.workflow import root_agent, route_triage

def _record(category: str) -> TicketTriage:
    return TicketTriage(
        category=category,
        urgency="medium",
        summary="Synthetic request ready for deterministic routing.",
        next_action="Send the validated record to one resolver."
    )

def test_workflow_is_constructed():
    assert root_agent.name == "support_ops_workflow"

def test_every_allowed_category_produces_a_route_event():
    for category in ("billing", "technical", "account", "general"):
        event = route_triage(_record(category))
        assert event.actions.route == category
```

**4. Run the workflow tests and full regression suite from the repository root, with work/ as pytest's working directory. If the Event representation changes in a later ADK version, inspect the object and update the assertion deliberately rather than weakening the route contract.**

```text
python -c "import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd='work').returncode)"
```

**5. Start ADK Web with the work/ agents directory and select support_ops.**

```text
adk web work
```

**6. Send a billing prompt. In the trace, verify the exact node order: triage_node, route_triage, billing_resolver. No other resolver should run.**

```text
I have two charges for one synthetic order. What evidence is needed?
```

**7. Send a technical prompt and confirm only technical_resolver runs after triage.**

```text
An idempotent API call timed out twice and I have the correlation ID.
```

**8. Send a general prompt that does not match the three specialist domains and confirm general_resolver handles it.**

```text
What information should a clear support ticket include?
```

**9. Try an ambiguous mixed-domain prompt. Record the triage category and ask whether one route is an acceptable process rule or whether the workflow needs a split or human decision node.**

```text
The customer cannot log in after a duplicate charge appeared.
```

**10. Switch work/support_ops/agent.py temporarily back to from .team import root_agent and repeat the mixed prompt. Compare flexible delegation with the graph's explicit single-route behaviour, then restore the workflow import.**

**11. Draw the production decision: use the coordinator for exploratory requests, the workflow for controlled processes, or a hybrid that places a coordinator inside bounded graph nodes.**

**12. Save the checkpoint for the MCP lab.**

```text
python -c "from pathlib import Path; Path('work/CHECKPOINT-LAB-06.txt').write_text('Typed graph routes and resolver isolation verified\n', encoding='utf-8')"
```

## Test It

From the repository root, the portable pytest command must pass. Each clear prompt must follow triage_node → route_triage → exactly one matching resolver, with the chosen category visible in the triage output. No ticket or knowledge tool should run in this controlled graph checkpoint because the resolver contract explicitly forbids claiming external work.

## Troubleshooting

- **The Workflow fails during import.** Confirm google-adk==2.5.0, import Agent, Event, and Workflow from google.adk, and keep every graph agent in single_turn mode.
- **A resolver cannot consume the triage output.** Confirm triage_agent.output_schema and resolver.input_schema both reference the same TicketTriage class.
- **An ambiguous request takes an unsafe route.** Tighten the triage labels or add an explicit clarification or human-input branch; do not rely on a longer resolver prompt to fix routing.

## Challenge

Add a deterministic urgent route before the domain router that emits human_review whenever urgency is high, and verify that no resolver runs until that branch is handled.

## Reflection

Which decisions in your SupportOps design require model judgement, and which should be encoded as graph structure or deterministic policy?

---

[← Lab 5](lab-05-build-a-specialist-agent-team.md) · [Lab 7 →](lab-07-discover-tools-through-mcp.md)
