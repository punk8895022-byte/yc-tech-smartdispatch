"""Fail-closed internal showcase intake tests. No network or external posting."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from release_gate import load, public_blockers, review_packet, validate_internal  # noqa: E402


class ReleaseGate(unittest.TestCase):
    def setUp(self):
        self.m = load()

    def test_01_initial_review_manifest_passes(self):
        self.assertEqual(validate_internal(self.m), [])

    def test_02_reject_owner_opening_without_permission(self):
        self.m["publishing"]["owner_gate"] = "APPROVED"
        self.assertTrue(validate_internal(self.m))

    def test_03_reject_fake_live_project(self):
        self.m["projects"][0]["display_status"] = "LIVE"
        self.assertTrue(validate_internal(self.m))

    def test_04_reject_external_posted_claim(self):
        self.m["projects"][0]["external_submission_status"] = "POSTED"
        self.assertTrue(validate_internal(self.m))

    def test_05_reject_fake_popularity(self):
        self.m["discovery"]["public_likes"] = True
        self.assertTrue(validate_internal(self.m))

    def test_06_reject_tracking(self):
        self.m["distribution"]["public_tracking"] = "ENABLED"
        self.assertTrue(validate_internal(self.m))

    def test_07_reject_duplicate_ids(self):
        self.m["projects"][1]["id"] = self.m["projects"][0]["id"]
        self.assertTrue(validate_internal(self.m))

    def test_08_reject_traversal_route(self):
        self.m["projects"][0]["route"] = "../private.html"
        self.assertTrue(validate_internal(self.m))

    def test_09_reject_unknown_category(self):
        self.m["projects"][0]["category"] = "unverified"
        self.assertTrue(validate_internal(self.m))

    def test_10_reject_missing_proof(self):
        self.m["projects"][1]["positioning"]["proof_statement"] = ""
        self.assertTrue(validate_internal(self.m))

    def test_11_reject_pii_review_prematurely_approved(self):
        self.m["projects"][1]["review_requirements"]["pii"] = "APPROVED"
        self.assertTrue(validate_internal(self.m))

    def test_12_public_release_is_always_outside_this_tool(self):
        self.assertIn("OWNER_SIGNOFF_MUST_BE_VERIFIED_OUTSIDE_THIS_SCRIPT",
                      public_blockers(self.m))
        self.assertIn("OWNER_GATE_CLOSED", public_blockers(self.m))

    def test_13_packet_names_two_projects_no_fake_social_proof(self):
        draft = review_packet(self.m)
        self.assertIn("XY-HD-001", draft)
        self.assertIn("CLOUDLINK-M1B", draft)
        self.assertIn("不對外發布", draft)
        self.assertNotIn("已有 216", draft)

    def test_14_reject_submissions_list(self):
        self.m["distribution"]["submissions"] = [{"platform": "IdeaX", "posted": True}]
        self.assertTrue(validate_internal(self.m))

    def test_15_reject_tracking_global_flag(self):
        self.m["publishing"]["tracking_enabled"] = True
        self.assertTrue(validate_internal(self.m))

    def test_16_reject_missing_limitations(self):
        self.m["projects"][0]["limitations"] = []
        self.assertTrue(validate_internal(self.m))


if __name__ == "__main__":
    unittest.main()
