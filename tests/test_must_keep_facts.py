"""Offline integrity checks for two meaning-preservation review fixtures.

These fixtures provide a human-review ledger for future generated replies. They do not
call a model and do not measure whether a model follows the skill.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_reply import check  # noqa: E402

FIXTURE = ROOT / "tests/fixtures/must_keep_facts.json"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: %s" % key)
        result[key] = value
    return result


def reject_nonstandard_constant(value):
    raise ValueError("non-standard JSON constant: %s" % value)


def load_fixture():
    return json.loads(
        FIXTURE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_nonstandard_constant,
    )


class MustKeepFactsFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_fixture()
        cls.cases = {case["id"]: case for case in cls.data["cases"]}

    def test_fixture_is_synthetic_and_has_two_distinct_cases(self):
        self.assertIn("synthetic", self.data["notice"].lower())
        self.assertIn("not model-evaluation results", self.data["notice"])
        self.assertEqual(
            set(self.cases),
            {"partial-success-unknown-cause", "exact-output-json"},
        )
        self.assertEqual(len(self.data["cases"]), len(self.cases))

    def test_partial_success_sample_preserves_every_fact_without_inventing_a_cause(self):
        case = self.cases["partial-success-unknown-cause"]
        reply = case["sample_reply"]

        for fact in case["must_keep_facts"]:
            with self.subTest(required_fact=fact):
                self.assertIn(fact.casefold(), reply.casefold())
        for unsupported_claim in case["must_not_claim"]:
            with self.subTest(unsupported_claim=unsupported_claim):
                self.assertNotIn(unsupported_claim.casefold(), reply.casefold())

        evidence = case["evidence"]
        self.assertEqual(evidence["tests_run"], evidence["tests_passed"] + evidence["tests_failed"])
        self.assertEqual(evidence["cause"], "not investigated")
        self.assertEqual(evidence["fix"], "none attempted")
        report = check(reply)
        self.assertTrue(report["ok"], report)

    def test_exact_json_sample_has_only_the_requested_keys_and_valid_values(self):
        case = self.cases["exact-output-json"]
        raw = case["exact_json"]
        self.assertEqual(raw, raw.strip())
        self.assertFalse(raw.startswith("```") or "**Conclusion:**" in raw)

        parsed = json.loads(
            raw,
            object_pairs_hook=unique_object,
            parse_constant=reject_nonstandard_constant,
        )
        self.assertEqual(list(parsed), case["required_keys_in_order"])
        self.assertEqual(parsed, case["evidence"])
        self.assertTrue(check(raw)["ok"], check(raw))

        with self.assertRaises(json.JSONDecodeError):
            json.loads(raw + "\nDone.")


if __name__ == "__main__":
    unittest.main()
