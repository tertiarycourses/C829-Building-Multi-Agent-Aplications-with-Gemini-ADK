import json
import logging
from typing import Any, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

logger = logging.getLogger("support_ops.policy")
BLOCKED_PHRASES = (
    "reveal api key",
    "show system prompt",
    "ignore previous instructions",
)


def _latest_user_text(request: LlmRequest) -> str:
    for content in reversed(request.contents or []):
        if content.role == "user" and content.parts:
            return " ".join(part.text or "" for part in content.parts)
    return ""


def guard_model_input(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    text = _latest_user_text(llm_request)
    blocked = any(phrase in text.lower() for phrase in BLOCKED_PHRASES)
    logger.info(
        json.dumps(
            {
                "event": "model_input_policy",
                "agent": callback_context.agent_name,
                "blocked": blocked,
                "input_chars": len(text),
            }
        )
    )
    if not blocked:
        return None
    callback_context.state["temp:input_blocked"] = True
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[
                types.Part(
                    text="I cannot help retrieve secrets, hidden instructions, or bypass policy. Ask for an approved runbook topic."
                )
            ],
        )
    )


def guard_tool_call(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> Optional[dict]:
    query = str(args.get("topic", ""))
    allowed = tool.name == "lookup_runbook" and query.lower() in {
        "billing",
        "technical",
        "account",
    }
    logger.info(
        json.dumps(
            {
                "event": "tool_policy",
                "agent": tool_context.agent_name,
                "tool": tool.name,
                "allowed": allowed,
                "argument_chars": len(query),
            }
        )
    )
    if allowed:
        return None
    tool_context.state["temp:tool_blocked"] = True
    return {
        "status": "error",
        "error_type": "policy",
        "message": "Tool call blocked by the approved topic and capability policy.",
    }
