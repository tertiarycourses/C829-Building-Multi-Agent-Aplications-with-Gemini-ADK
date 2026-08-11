"""Single source of truth for C829 courseware and connected labs."""

TITLE = "Building Multi Agent Aplications with Gemini ADK (C829)"
SHORT_TITLE = "Building Multi Agent Aplications with Gemini ADK (C829)"
COURSE_CODE = "C829"
VERSION = "v1.0"
VERSION_DATE = "11 August 2026"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "UEN: 201200696W"
TRAINER = "Tertiary Infotech Trainer"
DAYS = 2
MODE = "Instructor-led, hands-on practical labs"

# The published course duration is 15 hours over two days. Tea breaks are
# included in the scheduled learning time; the one-hour lunch is excluded.
DAY_MINUTES = 450
DAILY_TIMING = "9:30 am – 6:00 pm (1-hour lunch; tea breaks within scheduled time)"
DARK_THEME = False

LEARNING_OUTCOMES = [
    "LO1: Explain the ADK agent lifecycle and configure a Gemini agent with clear instructions, typed input or output, and session-aware behaviour.",
    "LO2: Build reliable function tools and API integrations with explicit schemas, validation, error handling, and safe secret management.",
    "LO3: Use session state and searchable memory to preserve relevant context without confusing conversation history, working state, and long-term knowledge.",
    "LO4: Design multi-agent systems with specialist roles, coordinator delegation, shared context, and deterministic graph workflows where control matters.",
    "LO5: Connect ADK agents to MCP capabilities and choose an appropriate routing strategy for tools, specialists, and workflow branches.",
    "LO6: Apply evaluation, observability, security guardrails, and deployment practices to prepare a multi-agent application for production use.",
]

LO_TITLES = [
    "Agent Foundations",
    "Reliable Tools",
    "State & Memory",
    "Agent Teams",
    "MCP & Routing",
    "Production Readiness",
]

TOPICS = [
    dict(
        num=1,
        code="01",
        title="Single Agent Foundations",
        subtitle="ADK architecture · Agent lifecycle · Gemini configuration · Structured I/O · Sessions",
        concepts=[
            ("ADK application anatomy", "An ADK app exposes a root_agent; a Runner coordinates model calls, tools, events, sessions, and the final response."),
            ("Lifecycle", "A user message enters a session, the agent reasons with Gemini, optional tools execute, events record the work, and a response returns."),
            ("Root agent contract", "The root_agent is the discoverable entry point used by adk web, adk run, the API server, and deployment targets."),
            ("Instruction versus description", "Instruction governs behaviour; description advertises capability so a coordinator can choose the right specialist."),
            ("Model selection", "Pin a stable model for reproducibility. Use a latest alias for exploration only when automatic upgrades are acceptable."),
            ("Structured I/O", "Pydantic schemas turn free-form model output into validated fields that code, tools, and later workflow nodes can consume."),
            ("Control nondeterminism", "Narrow scope, explicit policies, schemas, examples, and tests reduce variation without pretending an LLM is deterministic."),
            ("Events", "Events are the audit trail of messages, model responses, tool calls, tool results, state changes, and workflow progress."),
            ("Session", "A session is one conversation thread identified by app, user, and session IDs; it owns ordered events and temporary state."),
            ("Stateless or stateful", "Stateless calls are easier to scale; stateful interactions are needed when later turns depend on earlier choices or progress."),
            ("Worked example", "SupportOps converts a vague ticket into category, urgency, summary, and next_action—then stores the typed result for the next turn."),
            ("When one agent is enough", "Prefer one focused agent while one instruction set and one tool boundary remain understandable; split only when roles truly diverge."),
        ],
    ),
    dict(
        num=2,
        code="02",
        title="Tools, Memory and Sessions",
        subtitle="Function calling · External APIs · Tool errors · Session state · Long-term memory · Vector retrieval",
        concepts=[
            ("Tool contract", "A tool has a name, purpose, typed arguments, documented constraints, and a structured result the model can interpret."),
            ("Schemas from Python", "ADK inspects function names, type hints, defaults, and docstrings; ambiguous signatures create ambiguous tool calls."),
            ("Execution loop", "Gemini selects a tool, ADK validates arguments, application code executes it, and the result returns to the model for the next decision."),
            ("Read versus write tools", "Queries are lower risk. Mutating tools need authorisation, confirmation, idempotency, and a record of what changed."),
            ("Secrets", "Credentials belong in environment variables or a managed secret store—never source code, prompts, logs, screenshots, or tool results."),
            ("External API reliability", "Set timeouts, validate status and payload, retry only safe failures, respect rate limits, and preserve correlation IDs."),
            ("Errors as data", "Return a stable status and recoverable message so the agent can explain, retry safely, or ask for missing information."),
            ("Tool chaining", "Let each tool do one job and pass compact results forward; long chains multiply latency, cost, permissions, and failure modes."),
            ("State scopes", "Session state tracks one thread; user- and app-scoped prefixes support wider persistence when the selected service stores them."),
            ("Memory versus history", "History records what happened; state holds current working facts; memory is searchable knowledge across sessions or sources."),
            ("Vector retrieval", "Chunk documents, create embeddings, store vectors with metadata, retrieve top matches, then ground the response in returned evidence."),
            ("Use memory deliberately", "Store stable preferences and reusable facts, not every utterance. Apply retention, consent, access, and deletion rules."),
        ],
    ),
    dict(
        num=3,
        code="03",
        title="Multi-Agent Architecture",
        subtitle="Specialisation · Coordinator and hierarchy · Delegation · Shared context · Graph workflows",
        concepts=[
            ("Why multiple agents", "Split a system when distinct roles need different instructions, tools, permissions, models, ownership, or evaluation criteria."),
            ("Specialisation", "A specialist owns a narrow outcome and small tool surface. Clear boundaries improve reasoning, testing, and least privilege."),
            ("Coordinator pattern", "A coordinator receives the request, selects a specialist, supplies context, checks the result, and communicates one coherent answer."),
            ("Delegation signal", "ADK uses specialist names, descriptions, modes, and coordinator instructions to decide when and how work should be delegated."),
            ("Supervisor and hierarchy", "A supervisor governs several specialists; deeper hierarchies can scale ownership but add latency and harder failure analysis."),
            ("LLM-based routing", "Flexible for ambiguous language, but probabilistic. Use bounded labels, examples, fallbacks, and telemetry around routing decisions."),
            ("Rule-based routing", "Fast and predictable for explicit identifiers, permissions, or thresholds; brittle when language and intent are genuinely ambiguous."),
            ("Graph workflow", "ADK 2.x Workflow edges make order and branches explicit, mixing LLM agents with deterministic functions and typed node outputs."),
            ("Pipeline pattern", "A fixed classify → enrich → resolve → summarise sequence is appropriate when every request must pass the same controlled stages."),
            ("Shared invocation context", "Collaborating agents can share session state, but keys and ownership must be documented to prevent accidental overwrites."),
            ("Handoff contract", "Pass only the task, validated context, evidence, constraints, and expected output—not the coordinator's entire internal prompt."),
            ("Failure isolation", "Set budgets, timeouts, fallbacks, and escalation paths per specialist so one failing capability does not collapse the whole team."),
        ],
    ),
    dict(
        num=4,
        code="04",
        title="MCP and Production Design",
        subtitle="MCP discovery · Structured context · Routing · Observability · Guardrails · Deployment and scale",
        concepts=[
            ("MCP client and server", "An MCP server publishes capabilities; an ADK McpToolset acts as a client and adapts discovered tools for an agent."),
            ("Protocol primitives", "Tools perform actions, resources expose data, and prompts provide reusable interaction templates through declared schemas."),
            ("Capability discovery", "The client lists server tools at runtime, reads their schemas, and exposes only the approved subset to the model."),
            ("Structured context", "Typed arguments, results, metadata, identity, and correlation IDs create an inspectable context envelope between components."),
            ("Least-privilege filtering", "Use tool filters, read-only modes, scoped credentials, and separate servers so an agent sees only what its role needs."),
            ("Connection lifecycle", "Local stdio and remote HTTP transports have different scaling, authentication, timeout, and shutdown requirements."),
            ("Routing strategy", "Combine deterministic rules for policy with model routing for ambiguity; record the chosen route and why it was selected."),
            ("Observability", "Correlate logs, traces, metrics, events, model calls, tool calls, latency, token use, errors, and outcomes across one request."),
            ("Evaluation", "Test final answers, route choice, tool trajectories, safety behaviour, latency, and cost with representative multi-turn cases."),
            ("Guardrail layers", "Validate input, authorise tools, constrain arguments, inspect results, filter output, and require human approval for high-impact actions."),
            ("Threat model", "Plan for prompt injection, data exfiltration, excessive agency, confused deputy risks, poisoned memory, and unsafe tool chaining."),
            ("Deployment and scale", "Externalise state, package dependencies, add health checks, cap concurrency, manage quotas, and choose Agent Runtime, Cloud Run, GKE, or another container host."),
        ],
    ),
]

DAY_THEMES = {
    1: "Single Agents, Tools, State and Memory",
    2: "Multi-Agent Orchestration, MCP and Production Readiness",
}


def SCHEDULE(lab_titles):
    return {
        1: (DAY_THEMES[1], [
            ("9:30", "9:50", 20, "admin", "Welcome, environment check, course roadmap and learning outcomes"),
            ("9:50", "10:50", 60, "topic", "Topic 1 — " + TOPICS[0]["title"] + " (concepts, architecture and worked example)"),
            ("10:50", "11:05", 15, "break", "Tea break"),
            ("11:05", "12:05", 60, "lab", "Hands-on: " + lab_titles([1])),
            ("12:05", "13:00", 55, "lab", "Hands-on: " + lab_titles([2])),
            ("13:00", "14:00", 60, "lunch", "Lunch break"),
            ("14:00", "15:00", 60, "topic", "Topic 2 — " + TOPICS[1]["title"] + " (concepts, patterns and worked example)"),
            ("15:00", "15:15", 15, "break", "Tea break"),
            ("15:15", "16:20", 65, "lab", "Hands-on: " + lab_titles([3])),
            ("16:20", "17:40", 80, "lab", "Hands-on: " + lab_titles([4])),
            ("17:40", "18:00", 20, "recap", "Day 1 recap, troubleshooting clinic and reflection"),
        ]),
        2: (DAY_THEMES[2], [
            ("9:30", "9:45", 15, "admin", "Day 1 recap, checkpoint recovery and Day 2 orientation"),
            ("9:45", "10:45", 60, "topic", "Topic 3 — " + TOPICS[2]["title"] + " (concepts, pattern selection and worked example)"),
            ("10:45", "11:00", 15, "break", "Tea break"),
            ("11:00", "12:05", 65, "lab", "Hands-on: " + lab_titles([5])),
            ("12:05", "13:00", 55, "lab", "Hands-on: " + lab_titles([6])),
            ("13:00", "14:00", 60, "lunch", "Lunch break"),
            ("14:00", "15:00", 60, "topic", "Topic 4 — " + TOPICS[3]["title"] + " (concepts, production trade-offs and worked example)"),
            ("15:00", "15:15", 15, "break", "Tea break"),
            ("15:15", "16:20", 65, "lab", "Hands-on: " + lab_titles([7])),
            ("16:20", "17:40", 80, "lab", "Hands-on: " + lab_titles([8])),
            ("17:40", "18:00", 20, "recap", "Course recap, production checklist, action plan and Q&A"),
        ]),
    }


COURSE_OVERVIEW = dict(
    section_title="Course Fundamentals",
    concepts_title="The ADK System Model",
    concepts=[
        ("Agent", "A model-driven component with a role, instructions, tools, schemas, and optional sub-agents."),
        ("Runner", "The application engine that executes the agent and coordinates services across each invocation."),
        ("Tool", "A typed capability that lets an agent read data, calculate, call a service, or perform an approved action."),
        ("Event", "An ordered record of messages, calls, results, state changes, and workflow outputs."),
        ("Session", "One conversation thread, including its events and temporary state."),
        ("Memory", "Searchable knowledge beyond the active thread, often backed by a managed or vector service."),
        ("Workflow", "An explicit graph or programmatic control flow that combines deterministic logic and agent reasoning."),
        ("MCP", "A standard client-server protocol for discovering and calling external tools and context capabilities."),
        ("Guardrail", "A policy check that observes, blocks, changes, or requires approval around an agent action."),
        ("Trace", "Correlated telemetry that explains the route, model calls, tools, latency, errors, and result."),
    ],
    framework_title="The DESIGN Production Lens",
    framework=[
        ("D — Define", "Name the user outcome, non-goals, boundaries, and acceptable failure behaviour."),
        ("E — Encapsulate", "Give each agent and tool one clear responsibility with a typed contract."),
        ("S — Share selectively", "Pass only the state, memory, and evidence required for the current task."),
        ("I — Inspect", "Capture events, route decisions, tool calls, traces, cost, and outcome quality."),
        ("G — Guard", "Apply identity, least privilege, validation, approvals, and output controls in layers."),
        ("N — Normalise", "Package, evaluate, version, and deploy the same reproducible application across environments."),
    ],
    statement=dict(
        headline="More agents create more interfaces—not automatically more intelligence.",
        body="Split responsibilities only when the new boundary improves ownership, permissions, evaluation, or reliability. Every handoff must earn its cost.",
        kicker="ARCHITECTURE PRINCIPLE",
    ),
    pillars_title="What You Will Build",
    pillars=[
        ("Reliable Core", ["A typed Gemini triage agent", "Validated tools and recoverable errors", "Session state and searchable knowledge"]),
        ("Agent Team", ["Three least-privilege specialists", "Coordinator delegation", "A deterministic resolution workflow"]),
        ("Production Edge", ["MCP capability discovery", "Guardrails and observability", "Tests and container packaging"]),
    ],
    arc_title="How Every Lab Progresses",
    arc=[
        "Understand the architectural idea and the trade-off it addresses.",
        "Inspect the starting checkpoint and predict the behaviour before running it.",
        "Build one bounded capability using synthetic data and placeholder secrets.",
        "Verify the result with a command, expected output, or visible event trace.",
        "Record the checkpoint so the next lab can extend the same SupportOps system.",
    ],
)

LAB_SHOTS = {}

LG_INTRO = (
    "This Learner Guide accompanies Building Multi Agent Aplications with Gemini ADK (C829), "
    "a two-day, 15-hour course for developers, solution architects, automation practitioners, "
    "and technical product teams. It starts with a single Gemini agent and builds deliberately "
    "toward a production-minded multi-agent application rather than treating orchestration as a diagram-only exercise."
)

LG_INTRO2 = (
    "All eight labs extend one synthetic SupportOps scenario. You will classify service requests, "
    "call reliable tools, carry relevant context across turns, add specialist agents, define an explicit "
    "workflow, discover a tool through MCP, and finish with guardrails, telemetry, tests, and a container. "
    "The examples target Google ADK 2.5.0 and Gemini 3.6 Flash as available on 11 August 2026."
)

LG_SETUP = dict(
    needs=[
        "A Windows, macOS, or Linux laptop with Python 3.10 or later, Git, and a modern web browser.",
        "A Google AI Studio API key. Store it only in a local .env file as GOOGLE_API_KEY.",
        "A code editor such as Visual Studio Code with Python support.",
        "Docker Desktop or another Docker-compatible runtime for Lab 8.",
        "Internet access for installing Python packages and calling the Gemini API.",
        "The course repository cloned locally. All ticket, customer, and knowledge data in the labs is synthetic.",
    ],
    verify_text=(
        "From the repository root, create and activate a virtual environment, install starter/requirements.txt, "
        "then run the version checks below. The expected ADK package version is 2.5.0."
    ),
    verify_code="python --version\npython -m pip show google-adk\nadk --help\ndocker --version",
    conventions=[
        "Run commands from the repository root unless a step says otherwise.",
        "Replace placeholders such as <GOOGLE_API_KEY> locally; never commit or paste a real secret into a prompt.",
        "Use synthetic IDs such as TKT-1001 and USR-101. Do not use customer, employee, or production data.",
        "Keep one terminal for adk web and a second terminal for tests and file edits.",
        "If a model or dependency changes after the course, begin with the pinned requirements and migration notes before upgrading.",
    ],
)

LAB_NOTE = (
    "Use only the synthetic ticket, customer, and knowledge data supplied in this repository. "
    "Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git."
)

LG_WRAPUP = dict(
    title="Wrap-Up",
    intro=(
        "You have taken one application from a bounded single agent to a multi-agent, MCP-enabled system "
        "with explicit controls. The lasting skill is not the number of agents you created; it is knowing "
        "which responsibilities should be probabilistic, which must be deterministic, and where policy must intervene."
    ),
    sections=[
        dict(title="What You Can Now Do", bullets=[
            "Define and run a Gemini ADK agent with typed output and session-aware behaviour.",
            "Create reliable function tools and retrieval capabilities with safe error contracts.",
            "Design coordinator, specialist, and graph workflow patterns for different control needs.",
            "Connect to an MCP server with an approved tool filter.",
            "Add tests, guardrails, correlated telemetry, and reproducible container packaging.",
        ]),
        dict(title="Architecture Habits", bullets=[
            "Start with one agent and split only when a boundary improves the system.",
            "Treat every tool and handoff as a typed, observable contract.",
            "Keep conversation history, working state, and long-term memory conceptually separate.",
            "Use deterministic rules for policy and explicit process; reserve model routing for ambiguity.",
            "Evaluate routes and trajectories, not only fluent final answers.",
        ]),
        dict(title="Production Boundaries", bullets=[
            "Do not grant write access without identity, authorisation, confirmation, and audit evidence.",
            "Do not expose every MCP capability to every agent.",
            "Do not store secrets or sensitive payloads in prompts, state, memory, or telemetry.",
            "Do not deploy without timeouts, budgets, fallbacks, health checks, and operational ownership.",
        ]),
    ],
)

LG_NEXT_STEPS = [
    "Replace one synthetic read-only tool with a sandbox API owned by your team and preserve the same error contract.",
    "Create ten representative evaluation cases covering routing, tool use, refusal, and recovery.",
    "Map each agent and tool to an identity, credential scope, data classification, and human owner.",
    "Export traces to your organisation's observability platform and define latency, error, and quality alerts.",
    "Deploy the container to a non-production environment with an external session service and managed secrets.",
]

LG_GLOSSARY = [
    ("ADK", "Google Agent Development Kit, a code-first framework for agents, tools, workflows, sessions, memory, evaluation, and deployment."),
    ("Agent", "A model-driven component configured with a role, instructions, model, tools, schemas, callbacks, and optional sub-agents."),
    ("Runner", "The service that executes an agent and coordinates sessions, memory, artifacts, plugins, and events."),
    ("Event", "A structured record produced during an invocation, including messages, tool activity, state changes, and workflow output."),
    ("Session", "One ordered conversation thread for a particular application and user."),
    ("State", "Key-value working data associated with a session or a broader configured scope."),
    ("Memory", "Searchable long-term knowledge that may span completed sessions or external sources."),
    ("Tool", "A typed capability an agent can call to retrieve information, calculate, or perform an approved action."),
    ("Function calling", "The model's selection of a named tool and structured arguments for the application to execute."),
    ("Coordinator", "An agent that routes or delegates work to specialist agents and composes the user-facing outcome."),
    ("Workflow", "An explicit sequence, branch, loop, or dynamic control flow combining agents and deterministic code."),
    ("MCP", "Model Context Protocol, a client-server standard for discovering and invoking tools and other context capabilities."),
    ("Guardrail", "A policy control that observes, validates, blocks, modifies, or requests approval around an interaction."),
    ("Prompt injection", "Untrusted content that attempts to override instructions or induce unsafe actions or data disclosure."),
    ("Idempotency", "A property that allows an operation to be retried without causing duplicate effects."),
    ("Trace", "Correlated telemetry showing the steps, calls, latency, errors, and outcome of one request."),
    ("Evaluation trajectory", "The sequence of routing, model, and tool decisions compared with expected behaviour."),
    ("Vector retrieval", "Searching embedded content by semantic similarity and returning the closest evidence with metadata."),
]

VERSION_HISTORY = [
    ("1.0", VERSION_DATE, "Initial release aligned across slide deck, Learner Guide, Lesson Plan, and eight connected labs.", TRAINER),
]
