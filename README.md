# Gemini Codex Workflow

## Purpose
A project template and workflow for keeping Gemini CLI and Codex in sync with shared, durable context files and reliable session close-out.

## Status
- Phase: TITAN (Phase 6: The Neural Dashboard)
- Current focus: Process stabilization after Sentinel hardening (shared-write safety, quota-aware routing, and capability-aware closeout behavior).
- Next milestone: Begin P0 remediation from the Sentinel forensic backlog while preserving the validated reconcile/dashboard baseline.

## How This Repo Works
This project uses synchronized context files so Gemini CLI and Codex always read the same instructions.

- Canonical context: `PROJECT_CONTEXT.md`
- Synced context files: `AGENTS.md`, `GEMINI.md`
- Session log: `session-summary.md`

## Key Files
- `PROJECT_CONTEXT.md`: canonical project context
- `AGENTS.md` / `GEMINI.md`: generated copies for tool compatibility
- `session-summary.md`: append-only session log
- `docs/session-closer.md`: strict close-out procedure
- `docs/operations.md`: day-to-day workflow guide
- `docs/new-project-bootstrap.md`: how to start new projects
- `docs/bootstrap-strategy-playbook.md`: scenario playbook for bootstrapping different ways (research-first and existing-repo integration)
- `docs/codex-gemini-bridge.md`: Codex <-> Gemini bridge routing + helper usage
- `docs/gemini-codex-bridge.md`: Gemini <-> Codex bridge routing + helper usage
- `scripts/sync_context.sh`: sync context files (supports `--check`)
- `scripts/session_close.sh`: authoritative sync + git close-out helper
- `scripts/closeout_full.sh`: deterministic pre-check + dry-run-first close-out wrapper (+ push)
- `scripts/resume_right_now.sh`: compact restart snapshot (focus, latest session, git/context health)
- `scripts/gemini_bridge.sh`: stable Codex -> Gemini one-shot bridge (`default|work|research`)
- `scripts/codex_bridge.sh`: stable Gemini -> Codex one-shot bridge (`default|work|research`)
- `scripts/collaborate.sh`: optional wrapper around `session_close.sh`
- `scripts/bootstrap_project.sh`: creates a new project structure (`full` default, `lean` optional)
- `scripts/ci_check.sh`: CI-oriented non-mutating workflow checks (`sync_context --check` + `make check`)
- `scripts/validate_workflow.sh`: workflow regression checks
- `scripts/lint_shell.sh`: shell lint and formatting checks
- `Makefile`: command shortcuts (`sync`, `check`, `ci-check`, `close`, `closeall`, `closeoutai`, `resumerightnow`, `bootstrap`, `collaborate`, `askgemini`, `askcodex`, `bridgecheck`)
- `scripts/dashboard2_commander_bridge.py`: watches `/tmp/<SWARM_ID>/commander_metrics.json` and publishes dashboard2 alerts to the blackboard.
- `scripts/swarm_dashboard2.py`: optional Textual-powered HUD (requires `textual` + `rich`, see docs)
- `research/README.md`: provenance index for canonical reports vs generated swarm artifacts vs live-run test artifacts

## Quick Start
1) Edit `PROJECT_CONTEXT.md` with your real project details.
2) Run: `scripts/sync_context.sh`
3) Start Gemini or Codex in this directory.
4) At end of each work block, run:
   - `scripts/session_close.sh --message "Session: <summary> (<YYYY-MM-DD>)"`
   - or deterministic all-in close: `scripts/closeout_full.sh --message "Session: <summary> (<YYYY-MM-DD>)"`
   - fastest UX: `make closeoutai NOTE="<short summary>"`
  - capability rule: always attempt closeout first, and only fallback to manual terminal closeout on concrete `.git` permission failure in that specific run
  - monitor swarms via `make dashboard` (classic Bash HUD) or `make dashboard2` (Textual HUD, requires `pip install textual rich`). Use `python3 scripts/swarm_dashboard2.py --snapshot` or `make dashboard2 ARGS="--snapshot"` for automation; hit `d` inside dashboard2 to delegate and toggle Intent vs Blackboard before submitting, and `h` for the in-app legend. If no swarm exists, dashboard2 bootstraps a local session and auto-follows the newest active reconcile/swarm session when workers start. Dashboard2 pulses the Neural Pulse heartbeat faster with alternating green/yellow glow, streams `/tmp/<SWARM_ID>/dashboard2_timeline.log` and `/tmp/<SWARM_ID>/commander_metrics.json`, and now renders an animated starfield background layer while replaying the sparkline. Trigger the commander bridge (`make dashboard2-commander`) to relay alerts back to the blackboard.
5) Run verification anytime with: `make check` (or `make ci-check` for CI-friendly entrypoint).
6) Resume instantly anytime: `make resumerightnow`

## New Project Bootstrap
- Full profile (default):
  - `scripts/bootstrap_project.sh <project_dir>`
- Lean profile:
  - `scripts/bootstrap_project.sh <project_dir> --profile lean`

## External Interop Audit
- Historical machine-level bridge attempts, verified interop behavior, and rejected patterns are documented in:
  - `docs/external-agent-audit.md`
- Operational runbook (what to do day-to-day) is in:
  - `docs/operations.md`
- One-page command reference + daily usage example:
  - `docs/cheatsheet.md`
- Codex -> Gemini bridge details and phrase routing:
  - `docs/codex-gemini-bridge.md`
- Gemini -> Codex bridge details and phrase routing:
  - `docs/gemini-codex-bridge.md`
