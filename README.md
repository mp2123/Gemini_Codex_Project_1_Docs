# Gemini Codex Workflow: The Durable Context Engine

The **Gemini Codex Workflow** is a high-velocity, autonomous development ecosystem designed to keep Gemini CLI and Codex CLI in a state of perfect synchronization. It eliminates "context drift" by using a declarative, file-based context layer and an autonomous reconciliation loop.

## 1. The Mission: Why This Exists
In complex, multi-agent AI development, maintaining a shared memory across different sessions and models is the primary bottleneck. This repository provides:
- **Durable Memory:** Key decisions, architectural rules, and session history are persisted in markdown files, not chat history.
- **Autonomous Execution:** Agents don't just "talk"—they reconcile. The system moves the repository from its current state to a desired state defined in `INTENT.md`.
- **Model Interoperability:** Seamlessly hand off tasks between Gemini (Strategic/Research) and Codex (Implementation/Hardening).

## 2. The Autonomous Engine (How It Works)
The repository operates like a distributed system (e.g., Kubernetes) for AI development.

### Declarative Intent (`INTENT.md`)
You define the "Desired State" for the repository in `INTENT.md`. Agents treat this as their backlog and autonomously volunteer for tasks.

### The Reconciliation Loop (`scripts/reconcile.sh`)
The core engine (`make reconcile`) matches the repository's current state to the `INTENT.md` backlog.
- **Single-Owner Lock:** Prevents controller collisions.
- **Shared-Write Safety:** Defer conflicts when multiple agents target the same file.
- **Quota-Aware Routing:** Automatically pivots between models to bypass rate limits.

### The Blackboard Architecture (`blackboard/`)
Independent agents coordinate via a shared directory using **Atomic File Leases**. This allows swarms to scale without a central bottleneck.

## 3. Core Capabilities
- **Swarm Intelligence:** Launch parallel agents (`make swarm`) with macOS alerts and audio signals for result "harvesting."
- **The Neural Dashboard:** High-fidelity TUI (`make dashboard2`) for real-time observability of swarm health, token burn, and agent sentiment.
- **Bidirectional Bridges:** Consult Gemini from Codex (`make askgemini`) or delegate to Codex from Gemini (`make askcodex`) using verified local-shell bridges.
- **Mobile Operations (iCloud):** Issue directives from an iPhone (via iOS Shortcuts or the Files app) into the repo's internal **Mobile Bus** (`AI_Automation/`). This allows for seamless "iCloud Drop" remote control of the system from anywhere.
- **Local RAG-lite:** Instant semantic code search via `make ask`.
- **Deterministic Close-Out:** One-command session hardening (`make closeoutai`) that runs 6 automated gates (Sync, Check, Archive, Dry-Run, Commit, Push).

## 4. Engineering Standards & Scope
- **Constitution-First:** `PROJECT_CONTEXT.md` is the single source of truth.
- **Modular Scripts:** POSIX-compliant shell scripts + Python 3 standard library.
- **Knowledge Graphing:** Automatic conversion of session logs into a relational Markdown graph.
- **Minimal Dependencies:** Core workflow requires only standard CLI tools (git, grep, bash, python).

## 5. Quick Start: The "Golden Path"
1.  **Define Law:** Edit `PROJECT_CONTEXT.md` with your project vision and details.
2.  **Sync:** Run `scripts/sync_context.sh` (or `make sync`) to generate agent context files (`AGENTS.md`, `GEMINI.md`).
3.  **Engage Agents:** Start Gemini or Codex in this directory.
4.  **Declare Intent:** Add your specific tasks to `INTENT.md`.
5.  **Reconcile:** Run `make reconcile` (or `scripts/reconcile.sh`) and monitor via the Neural Dashboard.
6.  **Close Out:** At the end of each work block, harden progress with:
    - `scripts/session_close.sh --message "Session: <summary> (<YYYY-MM-DD>)"`
    - or deterministic all-in: `scripts/closeout_full.sh --message "Session: <summary> (<YYYY-MM-DD>)"`
    - or fastest UX: `make closeoutai NOTE="<short summary>"`
7.  **Verify:** Run `make check` (or `make ci-check`) to ensure zero context drift.
8.  **Resume:** Restart context instantly with `make resumerightnow`.

## 6. Repository Map
| Component | Purpose | Guide |
| :--- | :--- | :--- |
| `scripts/` | **The Toolbox:** Core automation and bridges. | [scripts/README.md](scripts/README.md) |
| `docs/` | **The Library:** In-depth operating manuals. | [docs/README.md](docs/README.md) |
| `roadmap/` | **The Future:** Strategic system roadmaps. | [docs/roadmap/system-roadmap.md](docs/roadmap/system-roadmap.md) |
| `blackboard/` | **The Neural Net:** Swarm coordination state. | [blackboard/README.md](blackboard/README.md) |
| `AI_Automation/` | **The Mobile Bus:** iPhone integration bus. | [AI_Automation/README.md](AI_Automation/README.md) |
| `research/` | **The Knowledge Base:** Reports and benchmarks. | [research/README.md](research/README.md) |
| `machine_configs/` | **The Global Layer:** Host-system configs & skills. | [machine_configs/README.md](machine_configs/README.md) |
| `tests/` | **The Quality Gate:** Regression and stress suite. | [tests/README.md](tests/README.md) |
| `templates/` | **The Seeds:** Starter files for new projects. | `templates/` |

---
## Getting Help
- Run `make help` for a list of all available commands.
- See `docs/cheatsheet.md` for a one-page command cookbook.
- Consult `docs/ai-navigation-guide.md` for agent operating protocols.
- Use `make doctor` to verify your environment health.
