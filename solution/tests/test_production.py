from support_ops.production import guarded_runbook_agent, root_agent


def test_production_root_preserves_multi_agent_and_mcp_paths():
    assert root_agent.name == "support_ops_production"
    assert {agent.name for agent in root_agent.sub_agents} == {
        "support_ops_coordinator",
        "guarded_runbook_specialist",
    }
    team = next(agent for agent in root_agent.sub_agents if agent.name == "support_ops_coordinator")
    assert {agent.name for agent in team.sub_agents} == {
        "billing_specialist",
        "technical_specialist",
        "account_specialist",
    }


def test_mcp_specialist_has_the_tool_policy_callback():
    assert guarded_runbook_agent.before_tool_callback is not None
    assert len(guarded_runbook_agent.tools) == 1
