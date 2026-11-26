import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from protocol import summary, validate  # noqa: E402


class ProtocolTests(unittest.TestCase):
    def base(self):
        return {
            "operation": "update_topic",
            "target": "HIST-0001 / T01 / 2027.1",
            "institution": "Example University",
            "term": "2027.1",
        }

    def test_valid_read_or_draft_request(self):
        result = summary(self.base())
        self.assertTrue(result["ready"])
        self.assertTrue(result["persistent_action"])
        self.assertTrue(result["approval_required"])
        self.assertFalse(result["approval_received"])

    def test_missing_scope_is_rejected(self):
        request = self.base()
        del request["target"]
        errors = validate(request)
        self.assertIn("missing required fields: target", errors)

    def test_notification_is_explicit_side_effect(self):
        request = self.base() | {"notify_email": True}
        result = summary(request)
        self.assertIn("notification_email", result["side_effects"])

    def test_formal_submission_requires_call_and_approval(self):
        request = self.base() | {"operation": "submit_proposal"}
        result = summary(request)
        self.assertFalse(result["ready"])
        self.assertIn("formal submission requires a named call", result["errors"])
        self.assertIn("formal submission requires explicit approval", result["errors"])

    def test_formal_submission_with_approval_is_ready(self):
        request = self.base() | {
            "operation": "submit_proposal",
            "call": "Example PIBIC 2027",
            "approval": True,
        }
        result = summary(request)
        self.assertTrue(result["ready"])
        self.assertIn("formal_submission", result["side_effects"])
        self.assertTrue(result["approval_received"])

    def test_invalid_boolean_is_rejected(self):
        request = self.base() | {"approval": "yes"}
        self.assertIn("approval must be boolean when present", validate(request))

    def test_cli_example_is_json_and_synthetic(self):
        example = Path(__file__).parents[1] / "examples" / "sample_operation.json"
        request = json.loads(example.read_text(encoding="utf-8"))
        self.assertEqual(request["institution"], "Example University")
        self.assertTrue(summary(request)["ready"])


if __name__ == "__main__":
    unittest.main()
