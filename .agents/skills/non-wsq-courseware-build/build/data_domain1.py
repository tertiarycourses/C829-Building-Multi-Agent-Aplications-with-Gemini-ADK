"""Topic 1 — Single Agent Foundations. Labs 1–2."""

DOMAIN1 = [
    dict(
        num=1,
        topic=1,
        title="Create the SupportOps Agent",
        objective="LO1: Explain the ADK lifecycle and configure a focused Gemini root agent.",
        desc=(
            "You create an isolated Python environment, configure a placeholder-based Gemini connection, "
            "inspect the ADK project contract, and run a minimal SupportOps agent in the ADK development web UI. "
            "The finished checkpoint proves the full user → Runner → agent → model → event → response path before "
            "tools, memory, or delegation add complexity."
        ),
        build="A clean work/ project containing a discoverable support_ops.root_agent and a captured first-turn event trace.",
        services="Python 3.10+, Google ADK 2.5.0, Gemini 3.6 Flash, ADK Web",
        duration="60 minutes",
        prerequisites=[
            "Clone the C829 repository and open a terminal at its root.",
            "Obtain a Google AI Studio API key, but do not paste it into source code or course documents.",
            "Confirm python --version reports Python 3.10 or later.",
        ],
        deck_steps=[
            ("Run the smallest complete path first: expose root_agent, start ADK Web, send one synthetic ticket, then inspect the event trace before adding more moving parts.", "adk web work"),
        ],
        steps=[
            ("Create a disposable working copy. All later labs extend work/; starter/ remains a clean recovery point.",
             "python -c \"import shutil; shutil.copytree('starter', 'work', dirs_exist_ok=True)\""),
            ("Create a virtual environment inside work/.",
             "python -m venv work/.venv"),
            ("Activate the environment for your shell, then upgrade pip.",
             "Windows PowerShell: work\\.venv\\Scripts\\Activate.ps1\nmacOS/Linux: source work/.venv/bin/activate\npython -m pip install --upgrade pip"),
            ("Install the pinned course dependencies. Pinning keeps the lab compatible with the code and screenshots used in class.",
             "python -m pip install -r work/requirements.txt\npython -m pip show google-adk"),
            ("Create the local environment file from the placeholder and open work/.env in your editor. Replace <GOOGLE_API_KEY> only in that ignored local file.",
             "python -c \"import shutil; shutil.copyfile('work/.env.example', 'work/.env')\"\nGOOGLE_API_KEY=<GOOGLE_API_KEY>\nGEMINI_MODEL=gemini-3.6-flash"),
            ("Inspect work/support_ops/agent.py. Identify the model, name, description, instruction, and root_agent variable.",
             "python -c \"print(open('work/support_ops/agent.py', encoding='utf-8').read())\""),
            ("Run the static contract tests before spending model quota. The portable wrapper runs pytest with work/ as its working directory, so the sibling support_ops package is importable from any repository location.",
             "python -c \"import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_agent_contract.py', '-q'], cwd='work').returncode)\""),
            ("Start the ADK development UI from the repository root, passing the work/ agents directory explicitly. Keep this terminal running.",
             "adk web work"),
            ("In the browser, select support_ops and send a synthetic request. Do not include any real user or ticket information.",
             "My checkout failed twice and I was charged both times. Please help me understand the next step."),
            ("In ADK Web 2.5, open the selected session's Events view and select the response event to reveal its detail inspector. Locate the user content, model request, model response, author, invocation identifier, and final text. Record which lifecycle stages occurred and which did not.", ""),
            ("Stop the server with Ctrl+C and save a checkpoint marker for the next lab.",
             "python -c \"from pathlib import Path; Path('work/CHECKPOINT-LAB-01.txt').write_text('SupportOps root agent and first trace verified\\n', encoding='utf-8')\""),
        ],
        test=(
            "Run the portable pytest wrapper from Step 6 and expect all tests to pass. In ADK Web, the prompt must return a helpful support-oriented response, "
            "and the event panel must show one user message followed by a model-generated response with no tool call. Confirm work/CHECKPOINT-LAB-01.txt exists."
        ),
        troubleshooting=[
            ("adk is not recognised.", "Confirm the work/.venv environment is active, then rerun python -m pip install -r work/requirements.txt."),
            ("ADK Web shows no support_ops application.", "From the repository root, run adk web work and confirm work/support_ops/__init__.py imports agent."),
            ("Gemini returns an authentication error.", "Check that work/.env contains GOOGLE_API_KEY with no quotes or spaces around the equals sign; never print the value."),
        ],
        challenge="Add one instruction that makes the agent ask for a ticket ID when the user refers to an existing case, then compare the event trace before and after the change.",
        reflection="Which parts of the first turn were controlled by your code, and which parts remained model-driven?",
    ),
    dict(
        num=2,
        topic=1,
        title="Add Structured Triage and Sessions",
        objective="LO1, LO3: Validate structured agent output and distinguish session events from session state.",
        desc=(
            "You replace free-form triage with a Pydantic contract, store the latest validated result through output_key, "
            "and inspect how two turns share one session. The lab demonstrates why structured output is an interface, not merely a formatting preference, "
            "and why an in-memory development session should not be mistaken for durable production storage."
        ),
        build="A typed TicketTriage response with category, urgency, summary, and next_action stored as latest_triage in the active session.",
        services="Google ADK, Pydantic, ADK Web session and event inspector, pytest",
        duration="55 minutes",
        prerequisites=[
            "Complete Lab 1 and retain the work/ directory.",
            "Confirm work/.env contains a working local GOOGLE_API_KEY placeholder replacement.",
            "Stop any previous adk web process before editing agent.py.",
        ],
        deck_steps=[
            ("Treat the model output as an API: validate four bounded fields, store the result under latest_triage, and inspect both the event history and the session state.", "output_schema=TicketTriage, output_key='latest_triage'"),
        ],
        steps=[
            ("Create work/support_ops/models.py with the triage contract. Literal values make downstream routing finite and testable.",
             r'''from typing import Literal
from pydantic import BaseModel, Field

class TicketTriage(BaseModel):
    category: Literal["billing", "technical", "account", "general"]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(min_length=8, max_length=180)
    next_action: str = Field(min_length=8, max_length=180)'''),
            ("Replace work/support_ops/agent.py with a structured triage agent. output_key asks ADK to place the validated result in session state.",
             r'''import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from .models import TicketTriage

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

root_agent = Agent(
    name="support_ops",
    model=MODEL,
    description="Classifies a synthetic service request into a bounded triage record.",
    instruction=(
        "Classify the user's service request. Use only the allowed category and urgency values. "
        "Summarise the issue without inventing facts. Recommend one safe next action; do not claim an action was completed."
    ),
    output_schema=TicketTriage,
    output_key="latest_triage",
)'''),
            ("Create work/tests/test_models.py so invalid route labels fail before they can enter later workflows.",
             r'''import pytest
from pydantic import ValidationError
from support_ops.models import TicketTriage

def test_valid_triage_record():
    record = TicketTriage(
        category="billing",
        urgency="high",
        summary="Duplicate charge reported by synthetic customer.",
        next_action="Verify the two transaction references."
    )
    assert record.category == "billing"

def test_unknown_category_is_rejected():
    with pytest.raises(ValidationError):
        TicketTriage(
            category="refunds",
            urgency="high",
            summary="This category is outside the contract.",
            next_action="Route through an approved category."
        )'''),
            ("Run all offline tests from the repository root while giving pytest work/ as its working directory. Fix syntax, imports, and schema failures before using Gemini.",
             "python -c \"import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd='work').returncode)\""),
            ("Start ADK Web again and select support_ops.",
             "adk web work"),
            ("Send a first request that clearly maps to billing and high urgency.",
             "Ticket TKT-1001 shows two card charges for one order and the customer cannot place another order."),
            ("Inspect the final response. Confirm it is valid JSON with exactly category, urgency, summary, and next_action; the labels must come from the schema.", ""),
            ("In ADK Web 2.5, open the selected session's State view and find latest_triage, then open Events and select the latest response. Compare mutable working state with the chronological event record.", ""),
            ("In the same session, send a second turn with a pronoun and a changed constraint. This checks whether the active thread carries context.",
             "It is not blocking checkout now. Lower the urgency and tell me what evidence to collect first."),
            ("Create a new session and repeat only the second turn. Observe that the pronoun no longer has a reliable antecedent. This is the difference between session-aware behaviour and a stateless call.", ""),
            ("Restart ADK Web. Confirm the development in-memory session is not a durability guarantee, then save the checkpoint.",
             "python -c \"from pathlib import Path; Path('work/CHECKPOINT-LAB-02.txt').write_text('Typed triage and session state verified\\n', encoding='utf-8')\""),
        ],
        test=(
            "From the repository root, the portable pytest command in Step 4 must pass. A billing prompt must return schema-valid JSON whose category is billing, and the ADK state panel must contain latest_triage. "
            "A second turn in the same session should use prior context; the same turn in a new session should require clarification."
        ),
        troubleshooting=[
            ("The model adds Markdown around the JSON.", "Keep output_schema configured and restart ADK Web after editing; verify you selected the current support_ops app."),
            ("Pydantic rejects the response repeatedly.", "Shorten the instruction, retain the exact Literal labels, and use a request that clearly matches one category."),
            ("latest_triage is absent.", "Confirm output_key is set on root_agent and inspect the state for the same session that produced the response."),
        ],
        challenge="Add an optional ticket_id field constrained to the pattern TKT- followed by four digits, and add one passing and one failing schema test.",
        reflection="When should a downstream component consume session state, and when should it read the immutable event history instead?",
    ),
]
