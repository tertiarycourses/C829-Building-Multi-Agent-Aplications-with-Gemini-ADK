from support_ops.models import TicketTriage
from support_ops.workflow import root_agent, route_triage


def _record(category: str) -> TicketTriage:
    return TicketTriage(
        category=category,
        urgency="medium",
        summary="Synthetic request ready for deterministic routing.",
        next_action="Send the validated record to one resolver.",
    )


def test_workflow_is_constructed():
    assert root_agent.name == "support_ops_workflow"


def test_every_allowed_category_produces_a_route_event():
    for category in ("billing", "technical", "account", "general"):
        event = route_triage(_record(category))
        assert event.actions.route == category
