# Lab 1 — Create the SupportOps Agent

**Course:** Building Multi Agent Aplications with Gemini ADK (C829)<br>
**Topic 1:** Single Agent Foundations<br>
**Maps to:** LO1: Explain the ADK lifecycle and configure a focused Gemini root agent.<br>
**Tools:** Python 3.10+, Google ADK 2.5.0, Gemini 3.6 Flash, ADK Web

**Version:** v1.0 (11 August 2026)<br>
**Duration:** 60 minutes

---

## Goal

You create an isolated Python environment, configure a placeholder-based Gemini connection, inspect the ADK project contract, and run a minimal SupportOps agent in the ADK development web UI. The finished checkpoint proves the full user → Runner → agent → model → event → response path before tools, memory, or delegation add complexity.

## What You Will Build

A clean work/ project containing a discoverable support_ops.root_agent and a captured first-turn event trace.

## Prerequisites

- Clone the C829 repository and open a terminal at its root.
- Obtain a Google AI Studio API key, but do not paste it into source code or course documents.
- Confirm python --version reports Python 3.10 or later.

> **Data note.** Use only the synthetic ticket, customer, and knowledge data supplied in this repository. Store GOOGLE_API_KEY in a local .env file, never in source code, prompts, screenshots, logs, or Git.

## Steps

**1. Create a disposable working copy. All later labs extend work/; starter/ remains a clean recovery point.**

```text
python -c "import shutil; shutil.copytree('starter', 'work', dirs_exist_ok=True)"
```

**2. Create a virtual environment inside work/.**

```text
python -m venv work/.venv
```

**3. Activate the environment for your shell, then upgrade pip.**

```text
Windows PowerShell: work\.venv\Scripts\Activate.ps1
macOS/Linux: source work/.venv/bin/activate
python -m pip install --upgrade pip
```

**4. Install the pinned course dependencies. Pinning keeps the lab compatible with the code and screenshots used in class.**

```text
python -m pip install -r work/requirements.txt
python -m pip show google-adk
```

**5. Create the local environment file from the placeholder and open work/.env in your editor. Replace <GOOGLE_API_KEY> only in that ignored local file.**

```text
python -c "import shutil; shutil.copyfile('work/.env.example', 'work/.env')"
GOOGLE_API_KEY=<GOOGLE_API_KEY>
GEMINI_MODEL=gemini-3.6-flash
```

**6. Inspect work/support_ops/agent.py. Identify the model, name, description, instruction, and root_agent variable.**

```text
python -c "print(open('work/support_ops/agent.py', encoding='utf-8').read())"
```

**7. Run the static contract tests before spending model quota. The portable wrapper runs pytest with work/ as its working directory, so the sibling support_ops package is importable from any repository location.**

```text
python -c "import subprocess, sys; raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_agent_contract.py', '-q'], cwd='work').returncode)"
```

**8. Start the ADK development UI from the repository root, passing the work/ agents directory explicitly. Keep this terminal running.**

```text
adk web work
```

**9. In the browser, select support_ops and send a synthetic request. Do not include any real user or ticket information.**

```text
My checkout failed twice and I was charged both times. Please help me understand the next step.
```

**10. In ADK Web 2.5, open the selected session's Events view and select the response event to reveal its detail inspector. Locate the user content, model request, model response, author, invocation identifier, and final text. Record which lifecycle stages occurred and which did not.**

**11. Stop the server with Ctrl+C and save a checkpoint marker for the next lab.**

```text
python -c "from pathlib import Path; Path('work/CHECKPOINT-LAB-01.txt').write_text('SupportOps root agent and first trace verified\n', encoding='utf-8')"
```

## Test It

Run the portable pytest wrapper from Step 6 and expect all tests to pass. In ADK Web, the prompt must return a helpful support-oriented response, and the event panel must show one user message followed by a model-generated response with no tool call. Confirm work/CHECKPOINT-LAB-01.txt exists.

## Troubleshooting

- **adk is not recognised.** Confirm the work/.venv environment is active, then rerun python -m pip install -r work/requirements.txt.
- **ADK Web shows no support_ops application.** From the repository root, run adk web work and confirm work/support_ops/__init__.py imports agent.
- **Gemini returns an authentication error.** Check that work/.env contains GOOGLE_API_KEY with no quotes or spaces around the equals sign; never print the value.

## Challenge

Add one instruction that makes the agent ask for a ticket ID when the user refers to an existing case, then compare the event trace before and after the change.

## Reflection

Which parts of the first turn were controlled by your code, and which parts remained model-driven?

---

[← Labs index](README.md) · [Lab 2 →](lab-02-add-structured-triage-and-sessions.md)
