# Building Multi Agent Aplications with Gemini ADK

Design, build and evaluate single- and multi-agent AI applications in Python with Google's Agent Development Kit (ADK) and Gemini.

| Course detail | Information |
|---|---|
| Course code | `C829` |
| Programme | Non-WSQ |
| Duration | 2 days · 15 hours (9:30am – 5:30pm) |
| Registration | [View course details and register](https://www.tertiarycourses.com.sg/building-multi-agent-aplications-with-gemini-adk.html) |
| Provider | Tertiary Infotech Academy Pte Ltd (UEN 201200696W) |

---

## About the course

Courseware and hands-on lab repository for *Building Multi Agent Aplications with Gemini ADK*,
built on Google's open-source [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
and the Gemini model family. Across 18 labs you move from a first ADK agent to tool-using agents,
multi-agent handoff, workflow agents (Sequential, Parallel, Loop, Agent-as-a-Tool), guardrails,
structured output, MCP, agentic RAG and a Streamlit app.

---

## Learning outcomes

| | Outcome |
|---|---|
| **LO1** | Analyze the range of LLM applications using Generative AI (GAI) and identify their industrial use cases |
| **LO2** | Establish Google Gemini GAI designs and assess improvements on engineering processes |
| **LO3** | Develop LLM applications and assess its feasibility |
| **LO4** | Evaluate the performance effectiveness of Retrieval Augmented Generation (RAG) |

---

## Topics covered

| Topic | Title | Labs |
|---|---|---|
| 1 | Overview of Agentic AI in Gemini ADK | 1–4 |
| 2 | Build A Multi Agent App with Gemini ADK | 5–12 |
| 3 | Build Agentic AI RAG in Gemini ADK | 13–15 |
| 4 | Build an Agentic AI App with Gemini Agent ADK and Streamlit | 16–18 |

---

## Quick Start

**Prerequisites:** Python 3.13+, [uv](https://docs.astral.sh/uv/), and a free Gemini API key from
[Google AI Studio](https://aistudio.google.com).

```bash
git clone https://github.com/tertiarycourses/C829-Building-Multi-Agent-Aplications-with-Gemini-ADK.git
cd C829-Building-Multi-Agent-Aplications-with-Gemini-ADK/labs
uv sync
```

Create a `.env` file in the `labs/` folder:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-google-api-key
OPENWEATHER_API_KEY=your-openweather-key   # optional, tool labs
TAVILY_API_KEY=your-tavily-key             # optional, search labs
```

> **Never commit your `.env` file or API keys.** It is git-ignored in this repository.

Run any agent:

```bash
uv run adk run <agent_folder>   # terminal chat
uv run adk web                  # browser IDE at http://localhost:8000
```

---

## Labs

| # | Lab | Agent folder | Topic |
|---|---|---|---|
| 1 | Set Up the Gemini ADK Environment and Get an API Key | [`lab01`](labs/lab01/README.md) | 1 |
| 2 | Build Your First ADK Agent — A Retail Banking Assistant | [`lab02`](labs/lab02/README.md) | 1 |
| 3 | Give an Agent Tools — Live Weather and Web Search | [`lab03`](labs/lab03/README.md) | 1 |
| 4 | Swap the Model — Running an ADK Agent on a Non-Gemini LLM | [`lab04`](labs/lab04/README.md) | 1 |
| 5 | Give an Agent Memory — Sessions, State and the Runner | [`lab05`](labs/lab05/README.md) | 2 |
| 6 | Inspect the Agent Loop — Events, Tool Calls and Final Responses | [`lab06`](labs/lab06/README.md) | 2 |
| 7 | Multi-Agent Handoff — Joke Generator to Translator | [`lab07`](labs/lab07/README.md) | 2 |
| 8 | Hierarchical Multi-Agent System — The Tutor Agent | [`lab08`](labs/lab08/README.md) | 2 |
| 9 | Sequential Workflow Agent — Singapore Transport Route Planner | [`lab09`](labs/lab09/README.md) | 2 |
| 10 | Add a Guardrail — Blocking Unsafe Requests with a Callback | [`lab10`](labs/lab10/README.md) | 2 |
| 11 | Structured Output — Forcing Valid JSON with Pydantic | [`lab11`](labs/lab11/README.md) | 2 |
| 12 | Connect External Tools with MCP — StreamableHTTP and SSE | [`lab12`](labs/lab12/README.md) | 2 |
| 13 | Load, Split and Embed Documents into a Vector Store | [`lab13`](labs/lab13/README.md) | 3 |
| 14 | Build the Agentic RAG Agent — Retrieval as a Tool | [`lab14`](labs/lab14/README.md) | 3 |
| 15 | Evaluate RAG Performance — Retrieval Quality and Groundedness | [`lab15`](labs/lab15/README.md) | 3 |
| 16 | Declarative Agents — Configuring a Multi-Agent System in YAML | [`lab16`](labs/lab16/README.md) | 4 |
| 17 | Ship the Agent as a Web App with Streamlit | [`lab17`](labs/lab17/README.md) | 4 |
| 18 | Capstone — Build Your Own Multi-Agent Application | [`lab18`](labs/lab18/README.md) | 4 |

Every lab is a **self-contained folder** holding its own agent script, data files and a
`README.md` lab sheet. See [labs/LABS.md](labs/LABS.md) for the full index.

---

## Core ADK Patterns

**Define an agent**

```python
from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer clearly and concisely.',
)
```

**Add a tool** — the docstring and type hints are the contract the model reads.

```python
def get_weather(city: str) -> dict:
    """Retrieves the current weather for a specified city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: status and result or error msg.
    """
    return {"status": "success", "report": "..."}

agent = Agent(..., tools=[get_weather])
```

**Multi-agent handoff**

```python
root_agent = Agent(
    name='root_agent',
    sub_agents=[math_tutor_agent, physics_tutor_agent, history_tutor_agent],
    instruction='Route each question to the right specialist.',
)
```

**Sequential workflow**

```python
from google.adk.agents import SequentialAgent

workflow = SequentialAgent(
    name='workflow_agent',
    sub_agents=[input_agent, research_agent, report_agent],
)
```

**Guardrail** — return `None` to allow, an `LlmResponse` to block.

```python
def block_keyword_guardrail(callback_context, llm_request):
    if "BLOCK" in last_user_message.upper():
        return LlmResponse(content=types.Content(
            role="model", parts=[types.Part(text="I cannot process this request.")]))
    return None

agent = Agent(..., before_model_callback=block_keyword_guardrail)
```

**Structured output** — note an agent with `output_schema` cannot also use tools.

```python
from pydantic import BaseModel

class Recipe(BaseModel):
    title: str
    ingredients: list[str]
    cooking_time: int

agent = Agent(..., output_schema=Recipe)
```

---

## Courseware (public package)

| Artifact | File |
|---|---|
| Trainer Slides | [Building Multi Agent Aplications with Gemini ADK-v1.0.pptx](<courseware/Building Multi Agent Aplications with Gemini ADK-v1.0.pptx>) |
| Learner Slides (PDF) | [Building Multi Agent Aplications with Gemini ADK-v1.0.pdf](<courseware/Building Multi Agent Aplications with Gemini ADK-v1.0.pdf>) |
| Lesson Plan | [LP-Building Multi Agent Aplications with Gemini ADK.docx](<courseware/LP-Building Multi Agent Aplications with Gemini ADK.docx>) |
| Lesson Plan (PDF) | [LP-Building Multi Agent Aplications with Gemini ADK.pdf](<courseware/LP-Building Multi Agent Aplications with Gemini ADK.pdf>) |
| Learner Guide | [LG-Building Multi Agent Aplications with Gemini ADK.docx](<courseware/LG-Building Multi Agent Aplications with Gemini ADK.docx>) |
| Learner Guide (PDF) | [LG-Building Multi Agent Aplications with Gemini ADK.pdf](<courseware/LG-Building Multi Agent Aplications with Gemini ADK.pdf>) |
| Learner Guide (Markdown) | [LG-Building Multi Agent Aplications with Gemini ADK.md](<LG-Building Multi Agent Aplications with Gemini ADK.md>) |

The **Learner Guide** carries the full step-by-step instructions for all 18 labs, plus reference
sections on core ADK patterns, evaluating a RAG pipeline, and assessing the feasibility of an
agent application.

The **Trainer Slides** (v1.0, 152 slides) teach each lab as a four-part unit — briefing →
process map → procedure with the actual commands → verification with troubleshooting — alongside
comparison matrices, decision maps, worked code examples and native charts. Slide transitions are
deliberately restrained (content fades, section dividers push), with click-through reveals on the
process maps so a stage can be discussed before the next appears.

**Distribution:** slides, Lesson Plan, Learner Guide and labs are published here. Any assessment
material and source references are kept private and are never committed to this repository.

---

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Google AI Studio](https://aistudio.google.com) — free Gemini API keys
- [Course page](https://www.tertiarycourses.com.sg/building-multi-agent-aplications-with-gemini-adk.html)
- [LMS / TMS](https://lms-tms.tertiaryinfotech.com)

## Support

**Tertiary Infotech Academy Pte Ltd** · UEN 201200696W
Email: enquiry@tertiaryinfotech.com · Tel: +65 6100 0613 · [tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.
