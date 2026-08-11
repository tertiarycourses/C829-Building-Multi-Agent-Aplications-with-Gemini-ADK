import httpx
import pytest
from fastapi import HTTPException

from support_ops import tools
from support_ops.mock_api import PriorityUpdate, SEEN_KEYS, TICKETS, change_priority


def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/tickets/TKT-9999":
        return httpx.Response(404, json={"detail": "ticket_not_found"})
    if request.method == "GET":
        return httpx.Response(
            200,
            json={"id": "TKT-1001", "priority": "high", "status": "open"},
        )
    if request.headers.get("Idempotency-Key") == "conflict-key-001":
        return httpx.Response(409, json={"detail": "idempotency_key_reused_for_different_operation"})
    return httpx.Response(
        200,
        json={
            "ticket": {"id": "TKT-1001", "priority": "medium", "status": "open"},
            "repeated": False,
            "idempotency_key": request.headers["Idempotency-Key"],
        },
    )


def setup_module():
    tools._client.close()
    tools._client = httpx.Client(
        transport=httpx.MockTransport(_handler), base_url="http://test"
    )


def test_invalid_id_stops_before_http():
    assert tools.get_ticket("1001")["error_type"] == "validation"


def test_get_ticket_success():
    assert tools.get_ticket("tkt-1001")["ticket"]["id"] == "TKT-1001"


def test_not_found_is_recoverable():
    assert tools.get_ticket("TKT-9999") == {
        "status": "error",
        "error_type": "not_found",
        "message": "TKT-9999 does not exist.",
    }


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
