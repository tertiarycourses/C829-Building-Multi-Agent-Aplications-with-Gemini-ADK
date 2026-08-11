import json
from pathlib import Path
from types import SimpleNamespace

from google.adk.models import LlmRequest
from google.genai import types

from support_ops.policy import guard_model_input, guard_tool_call


class State(dict):
    pass


def _cases():
    return json.loads(Path("eval_cases.json").read_text(encoding="utf-8"))["cases"]


def _request(text: str) -> LlmRequest:
    return LlmRequest(contents=[types.Content(role="user", parts=[types.Part(text=text)])])


def test_eval_catalogue_has_unique_complete_cases():
    cases = _cases()
    assert len(cases) >= 4
    assert len({case["id"] for case in cases}) == len(cases)
    assert all("prompt" in case and "blocked" in case for case in cases)
    assert any(case["blocked"] for case in cases)
    assert any(not case["blocked"] for case in cases)


def test_every_catalogue_case_runs_through_deterministic_policy():
    for case in _cases():
        context = SimpleNamespace(agent_name="support_ops_production", state=State())
        model_result = guard_model_input(context, _request(case["prompt"]))
        if case["expected_tool"] is None:
            assert case["blocked"] is True and model_result is not None, case["id"]
            continue
        assert model_result is None, case["id"]
        tool = SimpleNamespace(name=case["expected_tool"])
        tool_result = guard_tool_call(tool, {"topic": case["expected_topic"]}, context)
        assert (tool_result is not None) is case["blocked"], case["id"]
