import pytest
from pydantic import ValidationError

from support_ops.models import TicketTriage


def test_valid_triage_record():
    record = TicketTriage(
        category="billing",
        urgency="high",
        summary="Duplicate charge reported by synthetic customer.",
        next_action="Verify the two transaction references.",
    )
    assert record.category == "billing"


def test_unknown_category_is_rejected():
    with pytest.raises(ValidationError):
        TicketTriage(
            category="refunds",
            urgency="high",
            summary="This category is outside the contract.",
            next_action="Route through an approved category.",
        )
