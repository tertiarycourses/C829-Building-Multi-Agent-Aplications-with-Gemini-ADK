from mcp.server.fastmcp import FastMCP

mcp = FastMCP("supportops-runbook")

RUNBOOKS = {
    "billing": {
        "source": "MCP-RB-BILL-01",
        "text": "For duplicate charges collect both transaction references, timestamps, amount, and order ID before reconciliation.",
    },
    "technical": {
        "source": "MCP-RB-TECH-02",
        "text": "For an API timeout record the correlation ID, endpoint, UTC time, retry count, and whether the operation is idempotent.",
    },
    "account": {
        "source": "MCP-RB-ACCT-03",
        "text": "For suspected account takeover revoke active sessions and route to the account-security owner; do not change contact details.",
    },
}


@mcp.tool()
def lookup_runbook(topic: str) -> dict:
    """Return one synthetic SupportOps runbook passage for billing, technical, or account."""
    topic = topic.strip().lower()
    if topic not in RUNBOOKS:
        return {
            "status": "error",
            "allowed_topics": sorted(RUNBOOKS),
            "message": "Choose one allowed synthetic topic.",
        }
    return {"status": "success", "topic": topic, **RUNBOOKS[topic]}


if __name__ == "__main__":
    mcp.run(transport="stdio")
