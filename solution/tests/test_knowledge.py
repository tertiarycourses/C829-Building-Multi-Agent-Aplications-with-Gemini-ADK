from support_ops.knowledge import search_knowledge


def test_duplicate_charge_search_returns_billing_runbook():
    result = search_knowledge("duplicate card charge transaction reference", top_k=2)
    assert "RB-BILL-01" in {match["source"] for match in result["matches"]}


def test_search_rejects_empty_query():
    assert search_knowledge(" ")["error_type"] == "validation"


def test_top_k_is_bounded():
    assert len(search_knowledge("account password reset", top_k=99)["matches"]) <= 3
