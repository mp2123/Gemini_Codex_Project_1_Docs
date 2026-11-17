"""Synthetic, offline reconstruction of a durable-context verification pattern."""
import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

CONTEXT = 'Goal: summarize synthetic task counts.\nBoundary: no external actions.\n'
EXPECTED = {'open': 2, 'closed': 1}


def initialize(root):
    """Create only synthetic fixtures inside a caller-owned scratch directory."""
    for name in ('PROJECT_CONTEXT.md', 'AGENTS.md', 'GEMINI.md'):
        (root / name).write_text(CONTEXT, encoding='utf-8')
    (root / 'proposal.json').write_text(json.dumps(EXPECTED), encoding='utf-8')


def verify(root):
    """Return evidence, never approve or execute a release."""
    checks = []
    inputs = {}
    for name in ('PROJECT_CONTEXT.md', 'AGENTS.md', 'GEMINI.md', 'proposal.json'):
        path = root / name
        if path.is_symlink() or not path.is_file():
            checks.append({'check': 'required_input', 'file': name, 'passed': False})
            continue
        inputs[name] = path.read_bytes()
    if len(inputs) == 4:
        checks.append({'check': 'context_sync', 'passed':
                       inputs['PROJECT_CONTEXT.md'] == inputs['AGENTS.md'] == inputs['GEMINI.md']})
        try:
            proposal = json.loads(inputs['proposal.json'])
            accepted = (isinstance(proposal, dict) and set(proposal) == set(EXPECTED)
                        and all(type(proposal[k]) is int and proposal[k] == v
                                for k, v in EXPECTED.items()))
        except (ValueError, UnicodeError):
            accepted = False
        checks.append({'check': 'synthetic_acceptance', 'passed': accepted})
    passed = len(inputs) == 4 and all(c['passed'] for c in checks)
    # No claimed approval: successful checks merely prepare an unapproved handoff.
    return {'schema': 'durable-context-demo.v1', 'synthetic': True,
            'status': 'READY_FOR_HUMAN_REVIEW' if passed else 'BLOCKED',
            'checks': checks,
            'input_sha256': {k: hashlib.sha256(v).hexdigest() for k, v in sorted(inputs.items())},
            'human_approval': {'status': 'NOT_GRANTED', 'required_before_external_action': True},
            'external_actions_executed': [],
            'handoff': {'next_step': 'Review evidence; no release is performed by this demo.'} if passed else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=['pass', 'drift', 'missing', 'bad-output'], default='pass')
    args = parser.parse_args()
    with TemporaryDirectory(prefix='synthetic-context-') as directory:
        root = Path(directory)
        initialize(root)
        if args.scenario == 'drift':
            (root / 'AGENTS.md').write_text('Outdated synthetic goal.\n', encoding='utf-8')
        elif args.scenario == 'missing':
            (root / 'GEMINI.md').unlink()
        elif args.scenario == 'bad-output':
            (root / 'proposal.json').write_text('{"open": 99, "closed": 1}', encoding='utf-8')
        result = verify(root)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result['status'] == 'READY_FOR_HUMAN_REVIEW' else 1


if __name__ == '__main__':
    raise SystemExit(main())
