import os

from dotenv import load_dotenv
from google.adk import Agent

from .knowledge import search_knowledge
from .tools import get_ticket

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

billing_agent = Agent(
    name="billing_specialist",
    model=MODEL,
    mode="single_turn",
    description="Handles duplicate charges, invoices, payment evidence, and other synthetic billing questions.",
    instruction=(
        "Handle only billing work. Retrieve a synthetic ticket when an ID is present and search the runbook for procedure. "
        "Return facts, source IDs, missing evidence, and a recommended next step to the coordinator. Do not promise refunds."
    ),
    tools=[get_ticket, search_knowledge],
)

technical_agent = Agent(
    name="technical_specialist",
    model=MODEL,
    mode="single_turn",
    description="Handles login failures, API timeouts, diagnostics, and synthetic technical runbook questions.",
    instruction=(
        "Handle only technical diagnosis. Search the runbook, cite source IDs, separate observed facts from hypotheses, "
        "and return a bounded diagnostic next step. Do not change tickets or accounts."
    ),
    tools=[search_knowledge],
)

account_agent = Agent(
    name="account_specialist",
    model=MODEL,
    mode="single_turn",
    description="Handles account access, suspected takeover, and identity-protection guidance for synthetic users.",
    instruction=(
        "Handle only account access and security guidance. Search the runbook and prioritise containment. "
        "Do not change contact details, reveal secrets, or perform account actions. Return safe next steps and source IDs."
    ),
    tools=[search_knowledge],
)

root_agent = Agent(
    name="support_ops_coordinator",
    model=MODEL,
    description="Coordinates specialist help for synthetic service requests.",
    instruction=(
        "Clarify the user's goal, delegate domain work to exactly the relevant specialist, then present one coherent answer. "
        "Do not perform specialist work yourself. If the request spans domains, state the order and delegate one bounded task at a time. "
        "If no specialist owns the request, explain the boundary instead of inventing a route."
    ),
    sub_agents=[billing_agent, technical_agent, account_agent],
)
