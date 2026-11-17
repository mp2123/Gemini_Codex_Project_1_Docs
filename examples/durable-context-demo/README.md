# Runnable durable-context demo

A small, offline reconstruction of the context synchronization and verification pattern in Michael Panico's private Gemini/Codex workflow project. This is new demonstration code, not an export of the private implementation or its history.

## The problem

When work moves between coding agents or sessions, stale instructions and unverified outputs can be mistaken for completed work. This example makes those failures visible and blocks the handoff until its checks pass.

## Run it

Requires Python 3.9+ and its standard library only. From this directory:

```sh
python3 demo.py --scenario pass
python3 demo.py --scenario drift
python3 demo.py --scenario missing
python3 demo.py --scenario bad-output
python3 -m unittest -v
```

The passing scenario exits `0` and prints `READY_FOR_HUMAN_REVIEW`. The other scenarios intentionally exit `1` and print `BLOCKED`. These nonzero exits are expected demonstrations, not installation failures.

Every run creates and cleans its own temporary directory containing only synthetic fixtures. It does not read your project, call a model, access a network, use credentials, commit, push, deploy, or place trades. Its JSON receipt is printed to the terminal, not saved automatically.

## What happens

1. A synthetic project goal is written into a canonical context file and two agent-facing copies.
2. A fixed synthetic proposal stands in for an agent's output: two open tasks and one closed task. No real agent generates it.
3. Checks reject missing inputs, symbolic links, context drift, malformed output, incorrect counts, or unexpected fields.
4. Passing checks produce a handoff and input fingerprints; failed checks produce no handoff.
5. Both outcomes explicitly record `human_approval: NOT_GRANTED` and no external actions. Passing a test is not permission to release.

The tests exercise actual behavior, including all four CLI scenarios, missing inputs, drift, malformed output, repeatability, and preserving fixture contents. Input hashes identify the bytes checked; they do not prove authorship, authenticity, or approval.

## Contribution and attribution

Michael's broader project combines personal implementation work with AI-assisted development, workflow direction, review, debugging, and iteration. This standalone example was implemented with AI assistance at his request to illustrate a pattern from that project. It is not a claim that Michael independently wrote every line or that the full private system has passed these tests.

## Limits and safety boundary

This is an educational fixture runner, not a production agent orchestrator, security sandbox, secret scanner, authorization system, or complete release controller. It demonstrates deterministic checks and an explicitly pending human-review boundary. It does not implement approval or execute a release. The acceptance rule is deliberately tiny and fixed; it is not an analytics model. The symlink check is not a general defense against hostile concurrent filesystem changes. Private logs, transcripts, employer data, local configuration, credentials, and original repository history are not included.

## Validation

The seven standard-library unit tests passed when this example was prepared. Run them yourself to verify your checkout. A passing run validates this example's tested cases only, not every failure mode of the original private workflow.
