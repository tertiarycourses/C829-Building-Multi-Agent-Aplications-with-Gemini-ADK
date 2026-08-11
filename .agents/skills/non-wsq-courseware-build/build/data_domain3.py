"""Topic 3 — Multi-Agent Architecture. Labs 5–6."""

DOMAIN3 = [
    dict(
        num=5,
        topic=3,
        title="Build a Specialist Agent Team",
        objective="LO4: Design a coordinator with bounded billing, technical, and account specialists using clear delegation contracts.",
        desc=(
            "You split SupportOps into three least-privilege specialists and place them behind one coordinator. "
            "Each specialist has a narrow description, instruction, mode, and tool set; the coordinator owns user communication and delegation. "
            "You test obvious, ambiguous, and out-of-scope requests to see how model-driven routing behaves and where descriptions become part of the architecture."
        ),
        build="A collaborative ADK agent team whose coordinator delegates synthetic requests to billing, technical, or account specialists.",
        services="Google ADK collaborative agents, Gemini 3.6 Flash, specialist tools, ADK trace inspector",
        duration="65 minutes",
        prerequisites=[
            "Complete the Day 1 checkpoint through Lab 4.",
            "Retain work/support_ops/tools.py and knowledge.py; start the local ticket API only for ticket lookup prompts.",
            "Review the allowed responsibility and tool boundary for each specialist before coding.",
        ],
        deck_steps=[
            ("Make delegation legible: each specialist needs a distinct description, one responsibility, the smallest tool set, and automatic return to the coordinator after one bounded task.", "coordinator → billing | technical | account → coordinator → user"),
        ],
        steps=[
            ("Create work/support_ops/team.py with three specialists. mode=single_turn prevents a specialist from taking over the whole conversation and supports bounded return to the coordinator.",
             r'''import os
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
)'''),
            ("Replace work/support_ops/agent.py with the package entry point. ADK still discovers one root_agent even though the implementation now contains four agents.",
             "from .team import root_agent"),
            ("Create work/tests/test_team.py. These tests verify ownership and least-privilege tool allocation without calling Gemini.",
             r'''from support_ops.team import account_agent, billing_agent, root_agent, technical_agent

def _tool_names(agent):
    return {getattr(tool, "name", getattr(tool, "__name__", type(tool).__name__)) for tool in agent.tools}

def test_coordinator_has_three_distinct_specialists():
    assert {agent.name for agent in root_agent.sub_agents} == {
        "billing_specialist", "technical_specialist", "account_specialist"
    }

def test_only_billing_can_read_ticket_records():
    assert "get_ticket" in _tool_names(billing_agent)
    assert "get_ticket" not in _tool_names(technical_agent)
    assert "get_ticket" not in _tool_names(account_agent)

def test_all_specialists_are_bounded_single_turn_workers():
    assert all(agent.mode == "single_turn" for agent in root_agent.sub_agents)'''),
            ("Run the team contract tests and the full Day 1 regression suite from the repository root, with work/ as pytest's working directory.",
             "python -c \"import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd='work').returncode)\""),
            ("If you will test TKT-1001, start the local API from the repository root in terminal 1. Otherwise the knowledge-only prompts do not need it.",
             "python -m uvicorn --app-dir work support_ops.mock_api:app --host 127.0.0.1 --port 8765"),
            ("Start ADK Web with the work/ agents directory in terminal 2 and select support_ops.",
             "adk web work"),
            ("Send an obvious billing request. In the trace, identify the coordinator decision, billing_specialist invocation, tool calls, specialist return, and coordinator response.",
             "For synthetic ticket TKT-1001, what duplicate-charge evidence should I collect?"),
            ("Send an obvious technical request. Confirm the technical specialist can search knowledge but cannot retrieve or mutate tickets.",
             "Our idempotent API request timed out. What diagnostic evidence should I record before retrying?"),
            ("Send an account-security request. Confirm the account specialist prioritises containment and cites RB-SEC-04.",
             "A synthetic user reports a suspected account takeover. What should happen first?"),
            ("Test an ambiguous request and observe whether the coordinator asks a question or chooses a route. Improve one specialist description if the route is not defensible.",
             "The customer says access stopped after a payment problem. Help."),
            ("Test an out-of-scope request. The coordinator should state the boundary instead of delegating to the least-wrong specialist.",
             "Book a courier to collect a laptop tomorrow."),
            ("Save the checkpoint and write down one routing failure mode you observed.",
             "python -c \"from pathlib import Path; Path('work/CHECKPOINT-LAB-05.txt').write_text('Coordinator delegation and specialist boundaries verified\\n', encoding='utf-8')\""),
        ],
        test=(
            "From the repository root, the portable pytest command must pass. In ADK Web, the three obvious prompts must delegate to billing_specialist, technical_specialist, and account_specialist respectively. "
            "The technical and account traces must not contain get_ticket. The out-of-scope prompt must not be forced into an unrelated specialist."
        ),
        troubleshooting=[
            ("Every request stays with the coordinator.", "Make each specialist description distinct and capability-focused, restart ADK Web, and confirm root_agent.sub_agents contains all three objects."),
            ("The wrong specialist is selected.", "Remove overlapping phrases from descriptions and add a coordinator example or clarification rule for the ambiguous boundary."),
            ("A specialist does not return control.", "Confirm mode is exactly single_turn and that the specialist instruction asks for a bounded result to the coordinator."),
        ],
        challenge="Add a general_support specialist with no tools that only asks clarifying questions, then test whether it reduces forced routing without stealing clear domain requests.",
        reflection="What concrete benefit did each agent boundary provide—different tools, different policy, different evaluation, or only a different name?",
    ),
    dict(
        num=6,
        topic=3,
        title="Orchestrate a Deterministic Resolution Pipeline",
        objective="LO4, LO5: Build an ADK graph workflow that constrains classification, routing, and specialist execution through typed edges.",
        desc=(
            "You create a graph-based workflow for requests that must follow an explicit process. A typed triage agent emits one bounded category; "
            "a deterministic router converts that value into a graph route; and one single-turn resolver produces the final bounded guidance. "
            "You compare this reliable process with the flexible coordinator from Lab 5 and document when each pattern is appropriate."
        ),
        build="A SupportOps Workflow with explicit START → triage → route → specialist edges for billing, technical, account, and general requests.",
        services="Google ADK 2.x Workflow, Event routing, Pydantic schemas, Gemini specialist nodes, pytest",
        duration="55 minutes",
        prerequisites=[
            "Complete Lab 5 and keep team.py as the model-driven delegation example.",
            "Retain models.py with the TicketTriage schema from Lab 2.",
            "Understand that graph workflow agents use single-turn nodes and explicit input/output contracts.",
        ],
        deck_steps=[
            ("Use the graph when process control matters: typed triage creates one route label, a deterministic function emits that route, and only the matching resolver runs.", "START → triage_agent → route_triage → {billing | technical | account | general}"),
        ],
        steps=[
            ("Create work/support_ops/workflow.py. The triage node is model-driven, while route_triage and the edge map are deterministic application logic.",
             r'''import os
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
        (route_triage, {
            "billing": billing_resolver,
            "technical": technical_resolver,
            "account": account_resolver,
            "general": general_resolver,
        }),
    ],
)'''),
            ("Replace work/support_ops/agent.py so ADK runs the graph for this checkpoint. team.py remains available for comparison.",
             "from .workflow import root_agent"),
            ("Create work/tests/test_workflow.py to test the deterministic route function for every allowed category.",
             r'''from support_ops.models import TicketTriage
from support_ops.workflow import root_agent, route_triage

def _record(category: str) -> TicketTriage:
    return TicketTriage(
        category=category,
        urgency="medium",
        summary="Synthetic request ready for deterministic routing.",
        next_action="Send the validated record to one resolver."
    )

def test_workflow_is_constructed():
    assert root_agent.name == "support_ops_workflow"

def test_every_allowed_category_produces_a_route_event():
    for category in ("billing", "technical", "account", "general"):
        event = route_triage(_record(category))
        assert event.actions.route == category'''),
            ("Run the workflow tests and full regression suite from the repository root, with work/ as pytest's working directory. If the Event representation changes in a later ADK version, inspect the object and update the assertion deliberately rather than weakening the route contract.",
             "python -c \"import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd='work').returncode)\""),
            ("Start ADK Web with the work/ agents directory and select support_ops.",
             "adk web work"),
            ("Send a billing prompt. In the trace, verify the exact node order: triage_node, route_triage, billing_resolver. No other resolver should run.",
             "I have two charges for one synthetic order. What evidence is needed?"),
            ("Send a technical prompt and confirm only technical_resolver runs after triage.",
             "An idempotent API call timed out twice and I have the correlation ID."),
            ("Send a general prompt that does not match the three specialist domains and confirm general_resolver handles it.",
             "What information should a clear support ticket include?"),
            ("Try an ambiguous mixed-domain prompt. Record the triage category and ask whether one route is an acceptable process rule or whether the workflow needs a split or human decision node.",
             "The customer cannot log in after a duplicate charge appeared."),
            ("Switch work/support_ops/agent.py temporarily back to from .team import root_agent and repeat the mixed prompt. Compare flexible delegation with the graph's explicit single-route behaviour, then restore the workflow import.", ""),
            ("Draw the production decision: use the coordinator for exploratory requests, the workflow for controlled processes, or a hybrid that places a coordinator inside bounded graph nodes.", ""),
            ("Save the checkpoint for the MCP lab.",
             "python -c \"from pathlib import Path; Path('work/CHECKPOINT-LAB-06.txt').write_text('Typed graph routes and resolver isolation verified\\n', encoding='utf-8')\""),
        ],
        test=(
            "From the repository root, the portable pytest command must pass. Each clear prompt must follow triage_node → route_triage → exactly one matching resolver, with the chosen category visible in the triage output. "
            "No ticket or knowledge tool should run in this controlled graph checkpoint because the resolver contract explicitly forbids claiming external work."
        ),
        troubleshooting=[
            ("The Workflow fails during import.", "Confirm google-adk==2.5.0, import Agent, Event, and Workflow from google.adk, and keep every graph agent in single_turn mode."),
            ("A resolver cannot consume the triage output.", "Confirm triage_agent.output_schema and resolver.input_schema both reference the same TicketTriage class."),
            ("An ambiguous request takes an unsafe route.", "Tighten the triage labels or add an explicit clarification or human-input branch; do not rely on a longer resolver prompt to fix routing."),
        ],
        challenge="Add a deterministic urgent route before the domain router that emits human_review whenever urgency is high, and verify that no resolver runs until that branch is handled.",
        reflection="Which decisions in your SupportOps design require model judgement, and which should be encoded as graph structure or deterministic policy?",
    ),
]
