from support_ops.agent import root_agent


def test_root_agent_is_discoverable_and_narrow():
    assert root_agent.name == "support_ops"
    assert root_agent.model == "gemini-3.6-flash"
    assert list(root_agent.tools) == []


def test_instruction_does_not_claim_unavailable_actions():
    instruction = str(root_agent.instruction).lower()
    assert "do not claim" in instruction
    assert "synthetic" in instruction
