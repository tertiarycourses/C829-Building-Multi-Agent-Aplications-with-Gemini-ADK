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
