"""Pure, synthetic, read-only evidence-card contract tests; no TBM access."""
import unittest
from datetime import date

from lead_quality import LeadInputError, evaluate_public_lead

BASE = {
    "source_mode": "PUBLIC_MANUAL",
    "source_url": "https://www.taiwanbm.com.tw/example-public-case",
    "observed_on": "2026-11-05",
    "posted_on": "2026-11-03",
    "category": "cctv",
    "region": "台南市",
    "scope_confirmed": True,
    "budget_known": True,
    "deadline_known": True,
}

class LeadQualityTests(unittest.TestCase):
    def assess(self, **changes):
        return evaluate_public_lead({**BASE, **changes}, as_of=date(2026, 11, 5))

    def test_complete_candidate_is_still_review_only_not_bid_approved(self):
        out = self.assess()
        self.assertEqual((out.score, out.review_state), (100, "REVIEW_CANDIDATE"))
        self.assertFalse(out.executable)
        self.assertFalse(out.can_contact)
        self.assertFalse(out.can_bid)
        self.assertFalse(out.can_publish)
        self.assertFalse(out.can_sync)
        self.assertEqual(out.financial_status, "NOT_AVAILABLE")
        self.assertIn("IDENTITY_AND_CONSENT_NOT_VERIFIED", out.reason_codes)

    def test_relevance_is_fail_closed_for_nas_and_other_regions(self):
        for changes in ({"category": "nas"}, {"region": "高雄市"}, {"category": "access"}):
            out = self.assess(**changes)
            self.assertEqual((out.review_state, out.score), ("OUT_OF_SCOPE", 0))
            self.assertFalse(out.can_bid)

    def test_stale_or_unknown_date_not_treated_as_fresh(self):
        old = self.assess(posted_on="2026-08-10")
        unknown = self.assess(posted_on=None)
        self.assertEqual(old.review_state, "NEEDS_EVIDENCE")
        self.assertIn("STALE_OVER_30_DAYS", old.reason_codes)
        self.assertIn("POSTED_DATE_UNKNOWN", unknown.reason_codes)
        self.assertLess(old.score, 100)
        self.assertLess(unknown.score, 100)

    def test_missing_budget_scope_deadline_is_not_high_confidence(self):
        out = self.assess(budget_known=False, scope_confirmed=False, deadline_known=False)
        self.assertEqual(out.review_state, "NEEDS_EVIDENCE")
        self.assertIn("SCOPE_UNCONFIRMED", out.reason_codes)
        self.assertIn("BUDGET_UNKNOWN", out.reason_codes)
        self.assertIn("DEADLINE_UNKNOWN", out.reason_codes)
        self.assertLess(out.score, 70)

    def test_synthetic_case_cannot_be_commercial_lead(self):
        out = self.assess(source_mode="SYNTHETIC", source_url="https://example.com/fixture")
        self.assertIn("SYNTHETIC_NONCOMMERCIAL", out.reason_codes)
        self.assertFalse(out.can_contact)

    def test_rejects_url_credentials_private_address_and_query_tokens(self):
        for url in ("file:///etc/passwd", "http://127.0.0.1/private", "http://localhost/private",
                    "https://user:password@example.com/a", "https://example.com/?token=secret",
                    "https://example.com/path#secret", "https://example.invalid/path"):
            with self.subTest(url=url), self.assertRaises(LeadInputError):
                self.assess(source_url=url)

    def test_rejects_unexpected_fields_that_could_contain_customer_pii(self):
        with self.assertRaises(LeadInputError):
            evaluate_public_lead({**BASE, "customer_phone": "0912345678"}, as_of=date(2026,11,5))

    def test_rejects_future_or_inconsistent_dates(self):
        for changes in ({"observed_on": "2026-11-06"}, {"posted_on": "2026-11-07"},
                        {"posted_on": "2026-11-05", "observed_on": "2026-11-04"}):
            with self.subTest(changes=changes), self.assertRaises(LeadInputError):
                self.assess(**changes)

    def test_rejects_bools_as_strings_and_bad_modes(self):
        for changes in ({"budget_known": "yes"}, {"source_mode": "SCRAPED"},
                        {"category": 2}, {"observed_on": None}):
            with self.subTest(changes=changes), self.assertRaises(LeadInputError):
                self.assess(**changes)

    def test_no_personal_data_or_unverified_source_details_in_output(self):
        out = self.assess()
        self.assertFalse(hasattr(out, "source_url"))
        self.assertFalse(hasattr(out, "requester_name"))
        self.assertEqual(out.source_host, "www.taiwanbm.com.tw")
        self.assertEqual(out.source_mode, "PUBLIC_MANUAL")
        self.assertIn("PUBLIC_ACCESS_AND_RIGHTS_NOT_VERIFIED", out.reason_codes)

if __name__ == "__main__":
    unittest.main()
