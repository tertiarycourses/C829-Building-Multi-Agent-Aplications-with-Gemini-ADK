"""Lab 1 checkpoint: the smallest complete ADK agent."""

import os

from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

root_agent = Agent(
    name="support_ops",
    model=MODEL,
    description="Helps with synthetic service requests used in the C829 labs.",
    instruction=(
        "You are the SupportOps teaching agent. Work only with synthetic examples. "
        "Summarise the user's issue, state what information is missing, and recommend one safe next step. "
        "Do not claim to have looked up or changed a system because no tools are connected yet."
    ),
)
