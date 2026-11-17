"""Behavioral tests; no live agents, private inputs, credentials or network."""
import contextlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import demo


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        demo.initialize(self.root)

    def blocked(self):
        result = demo.verify(self.root)
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertIsNone(result['handoff'])
        self.assertEqual(result['external_actions_executed'], [])
        self.assertEqual(result['human_approval']['status'], 'NOT_GRANTED')

    def test_success_is_not_approval(self):
        result = demo.verify(self.root)
        self.assertEqual(result['status'], 'READY_FOR_HUMAN_REVIEW')
        self.assertEqual(result['human_approval']['status'], 'NOT_GRANTED')
        self.assertEqual(result['external_actions_executed'], [])
        self.assertEqual(len(result['input_sha256']), 4)

    def test_each_missing_file_blocks(self):
        for name in ('PROJECT_CONTEXT.md', 'AGENTS.md', 'GEMINI.md', 'proposal.json'):
            with self.subTest(name=name):
                demo.initialize(self.root)
                (self.root / name).unlink()
                self.blocked()

    def test_drift_blocks(self):
        (self.root / 'GEMINI.md').write_text('stale', encoding='utf-8')
        self.blocked()

    def test_bad_or_malformed_output_blocks(self):
        for value in ('{', 'null', '[]', '{"open": 99, "closed": 1}',
                      '{"open": 2, "closed": true}', '{"open": 2, "closed": 1, "extra": 0}'):
            with self.subTest(value=value):
                (self.root / 'proposal.json').write_text(value, encoding='utf-8')
                self.blocked()

    def test_symlink_rejected(self):
        (self.root / 'AGENTS.md').unlink()
        (self.root / 'AGENTS.md').symlink_to(self.root / 'PROJECT_CONTEXT.md')
        self.blocked()

    def test_repeatable_and_no_input_mutation(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(demo.verify(self.root), demo.verify(self.root))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_cli_exit_codes_and_receipts(self):
        for scenario in ('pass', 'drift', 'missing', 'bad-output'):
            with self.subTest(scenario=scenario):
                output = io.StringIO()
                with patch('sys.argv', ['demo.py', '--scenario', scenario]), contextlib.redirect_stdout(output):
                    code = demo.main()
                self.assertEqual(code, 0 if scenario == 'pass' else 1)
                self.assertEqual(json.loads(output.getvalue())['external_actions_executed'], [])


if __name__ == '__main__':
    unittest.main()
