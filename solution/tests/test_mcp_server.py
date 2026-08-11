from support_ops.mcp_server import lookup_runbook


def test_allowed_topic_returns_source_label():
    result = lookup_runbook("technical")
    assert result["status"] == "success"
    assert result["source"] == "MCP-RB-TECH-02"


def test_unknown_topic_is_bounded():
    result = lookup_runbook("payroll")
    assert result["status"] == "error"
    assert result["allowed_topics"] == ["account", "billing", "technical"]
