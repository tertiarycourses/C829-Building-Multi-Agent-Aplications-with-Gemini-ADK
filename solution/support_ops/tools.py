import os
import re
from typing import Literal

import httpx
from google.adk.tools.tool_context import ToolContext

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
    """Change a synthetic ticket priority after explicit user approval. Supply one stable idempotency key per requested change."""
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


def remember_response_style(style: Literal["concise", "detailed"], tool_context: ToolContext) -> dict:
    """Remember the user's preferred response style for later synthetic support conversations."""
    tool_context.state["user:response_style"] = style
    return {"status": "success", "response_style": style}


def get_response_style(tool_context: ToolContext) -> dict:
    """Read the user's stored response-style preference."""
    return {"status": "success", "response_style": tool_context.state.get("user:response_style", "concise")}
