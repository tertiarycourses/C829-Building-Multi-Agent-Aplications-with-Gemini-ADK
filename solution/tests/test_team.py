from support_ops.team import account_agent, billing_agent, root_agent, technical_agent


def _tool_names(agent):
    return {
        getattr(tool, "name", getattr(tool, "__name__", type(tool).__name__))
        for tool in agent.tools
    }


def test_coordinator_has_three_distinct_specialists():
    assert {agent.name for agent in root_agent.sub_agents} == {
        "billing_specialist",
        "technical_specialist",
        "account_specialist",
    }


def test_only_billing_can_read_ticket_records():
    assert "get_ticket" in _tool_names(billing_agent)
    assert "get_ticket" not in _tool_names(technical_agent)
    assert "get_ticket" not in _tool_names(account_agent)


def test_all_specialists_are_bounded_single_turn_workers():
    assert all(agent.mode == "single_turn" for agent in root_agent.sub_agents)
