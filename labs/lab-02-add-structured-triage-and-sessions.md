# Lab 2 — Add Structured Triage and Sessions

**Course:** Building Multi Agent Aplications with Gemini ADK (C829)<br>
**Topic 1:** Single Agent Foundations<br>
**Maps to:** LO1, LO3: Validate structured agent output and distinguish session events from session state.<br>
**Tools:** Google ADK, Pydantic, ADK Web session and event inspector, pytest

**Version:** v1.0 (11 August 2026)<br>
**Duration:** 55 minutes

---

## Goal

You replace free-form triage with a Pydantic contract, store the latest validated result through output_key, and inspect how two turns share one session. The lab demonstrates why structured output is an interface, not merely a formatting preference, and why an in-memory development session should not be mistaken for durable production storage.

## What You Will Build

A typed TicketTriage response with category, urgency, summary, and next_action stored as latest_triage in the active session.

## Prerequisites

- Complete Lab 1 and retain the work/ directory.
- Confirm work/.env contains a working local GOOGLE_API_KEY placeholder replacement.
- Stop any previous adk web process before editing agent.py.

> **Data note.** Use only the synthetic ticket, customer, and knowledge data supplied in this repository. Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git.

## Steps

**1. Create work/support_ops/models.py with the triage contract. Literal values make downstream routing finite and testable.**

```text
from typing import Literal
from pydantic import BaseModel, Field

class TicketTriage(BaseModel):
    category: Literal["billing", "technical", "account", "general"]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(min_length=8, max_length=180)
    next_action: str = Field(min_length=8, max_length=180)
```

**2. Replace work/support_ops/agent.py with a structured triage agent. output_key asks ADK to place the validated result in session state.**

```text
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from .models import TicketTriage

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

root_agent = Agent(
    name="support_ops",
    model=MODEL,
    description="Classifies a synthetic service request into a bounded triage record.",
    instruction=(
        "Classify the user's service request. Use only the allowed category and urgency values. "
        "Summarise the issue without inventing facts. Recommend one safe next action; do not claim an action was completed."
    ),
    output_schema=TicketTriage,
    output_key="latest_triage",
)
```

**3. Create work/tests/test_models.py so invalid route labels fail before they can enter later workflows.**

```text
import pytest
from pydantic import ValidationError
from support_ops.models import TicketTriage

def test_valid_triage_record():
    record = TicketTriage(
        category="billing",
        urgency="high",
        summary="Duplicate charge reported by synthetic customer.",
        next_action="Verify the two transaction references."
    )
    assert record.category == "billing"

def test_unknown_category_is_rejected():
    with pytest.raises(ValidationError):
        TicketTriage(
            category="refunds",
            urgency="high",
            summary="This category is outside the contract.",
            next_action="Route through an approved category."
        )
```

**4. Run all offline tests from the repository root while giving pytest work/ as its working directory. Fix syntax, imports, and schema failures before using Gemini.**

```text
python -c "import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd='work').returncode)"
```

**5. Start ADK Web again and select support_ops.**

```text
adk web work
```

**6. Send a first request that clearly maps to billing and high urgency.**

```text
Ticket TKT-1001 shows two card charges for one order and the customer cannot place another order.
```

**7. Inspect the final response. Confirm it is valid JSON with exactly category, urgency, summary, and next_action; the labels must come from the schema.**

**8. In ADK Web 2.5, open the selected session's State view and find latest_triage, then open Events and select the latest response. Compare mutable working state with the chronological event record.**

**9. In the same session, send a second turn with a pronoun and a changed constraint. This checks whether the active thread carries context.**

```text
It is not blocking checkout now. Lower the urgency and tell me what evidence to collect first.
```

**10. Create a new session and repeat only the second turn. Observe that the pronoun no longer has a reliable antecedent. This is the difference between session-aware behaviour and a stateless call.**

**11. Restart ADK Web. Confirm the development in-memory session is not a durability guarantee, then save the checkpoint.**

```text
python -c "from pathlib import Path; Path('work/CHECKPOINT-LAB-02.txt').write_text('Typed triage and session state verified\n', encoding='utf-8')"
```

## Test It

From the repository root, the portable pytest command in Step 4 must pass. A billing prompt must return schema-valid JSON whose category is billing, and the ADK state panel must contain latest_triage. A second turn in the same session should use prior context; the same turn in a new session should require clarification.

## Troubleshooting

- **The model adds Markdown around the JSON.** Keep output_schema configured and restart ADK Web after editing; verify you selected the current support_ops app.
- **Pydantic rejects the response repeatedly.** Shorten the instruction, retain the exact Literal labels, and use a request that clearly matches one category.
- **latest_triage is absent.** Confirm output_key is set on root_agent and inspect the state for the same session that produced the response.

## Challenge

Add an optional ticket_id field constrained to the pattern TKT- followed by four digits, and add one passing and one failing schema test.

## Reflection

When should a downstream component consume session state, and when should it read the immutable event history instead?

---

[← Lab 1](lab-01-create-the-supportops-agent.md) · [Lab 3 →](lab-03-connect-reliable-function-tools.md)
