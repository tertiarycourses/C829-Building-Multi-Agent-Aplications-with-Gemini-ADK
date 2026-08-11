import os

from dotenv import load_dotenv
from google.adk import Agent, Event, Workflow

from .models import TicketTriage

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

triage_agent = Agent(
    name="triage_node",
    model=MODEL,
    mode="single_turn",
    instruction=(
        "Classify the synthetic request into billing, technical, account, or general. "
        "Return urgency, a factual summary, and one safe next action."
    ),
    output_schema=TicketTriage,
)


def route_triage(record: TicketTriage):
    """Convert the validated category into a deterministic graph route."""
    return Event(route=record.category)


def _resolver(name: str, domain: str) -> Agent:
    return Agent(
        name=name,
        model=MODEL,
        mode="single_turn",
        input_schema=TicketTriage,
        output_schema=str,
        instruction=(
            f"You are the {domain} resolution node. Use only the supplied TicketTriage fields. "
            "Return: Route, Urgency, Known facts, Missing evidence, and Safe next step. "
            "Do not claim to have called a tool or changed a system."
        ),
    )


billing_resolver = _resolver("billing_resolver", "billing")
technical_resolver = _resolver("technical_resolver", "technical")
account_resolver = _resolver("account_resolver", "account")
general_resolver = _resolver("general_resolver", "general support")

root_agent = Workflow(
    name="support_ops_workflow",
    edges=[
        ("START", triage_agent, route_triage),
        (
            route_triage,
            {
                "billing": billing_resolver,
                "technical": technical_resolver,
                "account": account_resolver,
                "general": general_resolver,
            },
        ),
    ],
)
