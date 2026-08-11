# Lab 3 — Connect Reliable Function Tools

**Course:** Building Multi Agent Aplications with Gemini ADK (C829)<br>
**Topic 2:** Tools, Memory and Sessions<br>
**Maps to:** LO2: Build typed read and write tools around an external API with validation, timeouts, idempotency, and recoverable errors.<br>
**Tools:** Google ADK Function Tools, FastAPI, Uvicorn, HTTPX, pytest

**Version:** v1.0 (11 August 2026)<br>
**Duration:** 65 minutes

---

## Goal

You run a local synthetic support API, wrap it with ADK function tools, and give the agent a deliberately small capability surface. The read path validates identifiers and normalises HTTP failures; the write path requires an idempotency key and explicit user intent. This creates a tool contract the model can reason about without receiving credentials or raw exceptions.

## What You Will Build

A tool-enabled SupportOps agent that can retrieve a synthetic ticket and safely change its priority through a local HTTP API.

## Prerequisites

- Complete Lab 2 and retain work/support_ops/models.py for later workflow use.
- Confirm the work/.venv environment is active and no process is using port 8765.
- Use only the supplied synthetic ticket identifiers TKT-1001 through TKT-1003.

> **Data note.** Use only the synthetic ticket, customer, and knowledge data supplied in this repository. Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git.

## Steps

**1. Create work/support_ops/mock_api.py. The API is local and synthetic, but it behaves like a separate service boundary.**

```text
from typing import Literal
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Synthetic Support API")

TICKETS = {
    "TKT-1001": {"id": "TKT-1001", "subject": "Duplicate card charge", "priority": "high", "status": "open"},
    "TKT-1002": {"id": "TKT-1002", "subject": "Cannot reset password", "priority": "medium", "status": "open"},
    "TKT-1003": {"id": "TKT-1003", "subject": "Invoice address correction", "priority": "low", "status": "pending"},
}
SEEN_KEYS: dict[str, tuple[str, str]] = {}

class PriorityUpdate(BaseModel):
    priority: Literal["low", "medium", "high"]

@app.get("/tickets/{ticket_id}")
def read_ticket(ticket_id: str):
    ticket = TICKETS.get(ticket_id.upper())
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    return ticket

@app.patch("/tickets/{ticket_id}/priority")
def change_priority(ticket_id: str, body: PriorityUpdate, idempotency_key: str = Header()):
    ticket_id = ticket_id.upper()
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    operation = (ticket_id, body.priority)
    previous = SEEN_KEYS.get(idempotency_key)
    if previous is not None and previous != operation:
        raise HTTPException(status_code=409, detail="idempotency_key_reused_for_different_operation")
    repeated = idempotency_key in SEEN_KEYS
    if not repeated:
        ticket["priority"] = body.priority
        SEEN_KEYS[idempotency_key] = operation
    return {"ticket": ticket, "repeated": repeated, "idempotency_key": idempotency_key}
```

**2. Create work/support_ops/tools.py. Notice that a tool returns stable status data instead of leaking an HTTP exception into the model loop.**

```text
import os
import re
from typing import Literal
import httpx

BASE_URL = os.getenv("SUPPORT_API_URL", "http://127.0.0.1:8765")
_client = httpx.Client(timeout=httpx.Timeout(5.0))

def _valid_ticket_id(ticket_id: str) -> bool:
    return bool(re.fullmatch(r"TKT-\d{4}", ticket_id.strip().upper()))

def get_ticket(ticket_id: str) -> dict:
    """Retrieve one synthetic ticket by an ID such as TKT-1001."""
    ticket_id = ticket_id.strip().upper()
    if not _valid_ticket_id(ticket_id):
        return {"status": "error", "error_type": "validation", "message": "Use TKT- followed by four digits."}
    try:
        response = _client.get(f"{BASE_URL}/tickets/{ticket_id}")
        if response.status_code == 404:
            return {"status": "error", "error_type": "not_found", "message": f"{ticket_id} does not exist."}
        response.raise_for_status()
        return {"status": "success", "ticket": response.json()}
    except httpx.TimeoutException:
        return {"status": "error", "error_type": "timeout", "message": "The support API timed out; retry later."}
    except httpx.HTTPError:
        return {"status": "error", "error_type": "upstream", "message": "The support API is unavailable."}

def update_ticket_priority(
    ticket_id: str,
    priority: Literal["low", "medium", "high"],
    idempotency_key: str,
) -> dict:
    """Change a synthetic ticket priority after the user explicitly requests it. Supply one stable idempotency key per requested change."""
    ticket_id = ticket_id.strip().upper()
    if not _valid_ticket_id(ticket_id):
        return {"status": "error", "error_type": "validation", "message": "Use TKT- followed by four digits."}
    if len(idempotency_key.strip()) < 8:
        return {"status": "error", "error_type": "validation", "message": "The idempotency key must contain at least eight characters."}
    try:
        response = _client.patch(
            f"{BASE_URL}/tickets/{ticket_id}/priority",
            json={"priority": priority},
            headers={"Idempotency-Key": idempotency_key.strip()},
        )
        if response.status_code == 404:
            return {"status": "error", "error_type": "not_found", "message": f"{ticket_id} does not exist."}
        if response.status_code == 409:
            return {"status": "error", "error_type": "idempotency_conflict", "message": "Use one idempotency key for one exact requested change."}
        response.raise_for_status()
        return {"status": "success", **response.json()}
    except httpx.TimeoutException:
        return {"status": "error", "error_type": "timeout", "message": "The support API timed out; do not assume the write failed."}
    except httpx.HTTPError:
        return {"status": "error", "error_type": "upstream", "message": "The support API is unavailable."}
```

**3. Replace work/support_ops/agent.py with a tool-enabled agent. The instruction separates read behaviour from write behaviour.**

```text
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from .tools import get_ticket, update_ticket_priority

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

root_agent = Agent(
    name="support_ops",
    model=MODEL,
    description="Investigates synthetic support tickets and performs approved priority changes.",
    instruction=(
        "Work only with synthetic ticket IDs. Retrieve a ticket before discussing its current fields. "
        "Call update_ticket_priority only when the user explicitly asks to change priority and supplies or approves a change. "
        "Use one stable idempotency key for retries. Explain tool errors; never claim a write succeeded when status is error."
    ),
    tools=[get_ticket, update_ticket_priority],
)
```

**4. Archive the Lab 1 point-in-time agent contract before the agent gains tools. This preserves the evidence without making a deliberately obsolete test fail the evolving regression suite.**

```text
python -c "from pathlib import Path; import shutil; dst=Path('work/checkpoints'); dst.mkdir(exist_ok=True); src=Path('work/tests/test_agent_contract.py'); src.exists() and shutil.move(src, dst/'agent_contract_lab1.py.txt')"
```

**5. Create work/tests/test_tools.py with an HTTPX mock transport. The tests exercise success, validation, not-found, and idempotent-retry semantics without starting a real server.**

```text
import httpx
import pytest
from fastapi import HTTPException
from support_ops import tools
from support_ops.mock_api import PriorityUpdate, SEEN_KEYS, TICKETS, change_priority

def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/tickets/TKT-9999":
        return httpx.Response(404, json={"detail": "ticket_not_found"})
    if request.method == "GET":
        return httpx.Response(200, json={"id": "TKT-1001", "priority": "high", "status": "open"})
    if request.headers.get("Idempotency-Key") == "conflict-key-001":
        return httpx.Response(409, json={"detail": "idempotency_key_reused_for_different_operation"})
    return httpx.Response(200, json={
        "ticket": {"id": "TKT-1001", "priority": "medium", "status": "open"},
        "repeated": False,
        "idempotency_key": request.headers["Idempotency-Key"],
    })

def setup_module():
    tools._client.close()
    tools._client = httpx.Client(transport=httpx.MockTransport(_handler), base_url="http://test")

def test_invalid_id_stops_before_http():
    result = tools.get_ticket("1001")
    assert result["error_type"] == "validation"

def test_get_ticket_success():
    result = tools.get_ticket("tkt-1001")
    assert result["ticket"]["id"] == "TKT-1001"

def test_not_found_is_recoverable():
    result = tools.get_ticket("TKT-9999")
    assert result == {"status": "error", "error_type": "not_found", "message": "TKT-9999 does not exist."}

def test_write_carries_idempotency_key():
    result = tools.update_ticket_priority("TKT-1001", "medium", "lab3-change-001")
    assert result["status"] == "success"
    assert result["idempotency_key"] == "lab3-change-001"

def test_tool_surfaces_idempotency_conflict():
    result = tools.update_ticket_priority("TKT-1002", "high", "conflict-key-001")
    assert result["error_type"] == "idempotency_conflict"

def test_idempotency_key_is_bound_to_one_exact_operation():
    SEEN_KEYS.clear()
    TICKETS["TKT-1001"]["priority"] = "high"
    TICKETS["TKT-1002"]["priority"] = "medium"
    first = change_priority("TKT-1001", PriorityUpdate(priority="medium"), "one-operation-001")
    repeated = change_priority("TKT-1001", PriorityUpdate(priority="medium"), "one-operation-001")
    with pytest.raises(HTTPException) as conflict:
        change_priority("TKT-1002", PriorityUpdate(priority="high"), "one-operation-001")
    assert first["repeated"] is False
    assert repeated["repeated"] is True
    assert conflict.value.status_code == 409
    assert TICKETS["TKT-1002"]["priority"] == "medium"
```

**6. Review the bounded application-source delta before testing. The command intentionally excludes work/.venv, work/.env, and generated evidence. git diff --no-index returns status 1 when it displays differences; review the output before continuing.**

```text
git diff --no-index -- starter/support_ops work/support_ops
```

**7. Run the offline tool tests from the repository root, with work/ as pytest's working directory.**

```text
python -c "import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_tools.py', '-q'], cwd='work').returncode)"
```

**8. In terminal 1 at the repository root, start the synthetic API and leave it running.**

```text
python -m uvicorn --app-dir work support_ops.mock_api:app --host 127.0.0.1 --port 8765
```

**9. In terminal 2 at the repository root, activate the same environment and verify the API directly before involving the model.**

```text
python -c "import httpx; print(httpx.get('http://127.0.0.1:8765/tickets/TKT-1001', timeout=5).json())"
```

**10. Start ADK Web with the work/ agents directory in terminal 2.**

```text
adk web work
```

**11. Ask for a read-only lookup. Inspect the trace and confirm get_ticket is the only tool called.**

```text
Look up synthetic ticket TKT-1001 and tell me its current priority and status.
```

**12. Ask for an explicit write. Inspect the arguments and result of update_ticket_priority, including the idempotency key.**

```text
Change TKT-1001 priority to medium. Use idempotency key lab3-change-001.
```

**13. Repeat the exact write. The API should report repeated=true and leave the priority at medium instead of applying a duplicate effect.**

```text
Repeat the same priority change for TKT-1001 with idempotency key lab3-change-001.
```

**14. Stop the API and request another read. Confirm the agent reports an upstream error and does not invent ticket data. Save the checkpoint after the test.**

```text
python -c "from pathlib import Path; Path('work/CHECKPOINT-LAB-03.txt').write_text('External tools and safe write path verified\n', encoding='utf-8')"
```

## Test It

From the repository root, the portable pytest command must pass. With the local API running, the agent must retrieve TKT-1001, change its priority to medium, and return repeated=true when the same idempotency key is reused. With the API stopped, the agent must report unavailability without inventing fields.

## Troubleshooting

- **Port 8765 is already in use.** Stop the previous Uvicorn process or set SUPPORT_API_URL and the Uvicorn port to the same unused value.
- **The agent talks about a ticket without calling get_ticket.** Strengthen the instruction that current fields must come from the tool, restart ADK Web, and inspect the selected application.
- **A retry changes data twice.** Reuse exactly the same idempotency key; a new key represents a new requested operation.

## Challenge

Add a read-only list_open_tickets(priority) API endpoint and tool. Write an offline test before exposing it to root_agent.

## Reflection

Why should a timeout after a write be handled differently from a timeout before a read?

---

[← Lab 2](lab-02-add-structured-triage-and-sessions.md) · [Lab 4 →](lab-04-add-searchable-knowledge-and-memory.md)
