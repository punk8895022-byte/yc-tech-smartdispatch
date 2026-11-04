"""Synthetic-only tests for the reporting (not accounting-approval) contract."""
import unittest
from ledger_integrity import audit


def row(**overrides):
    d = dict(case_id="SYN-01", stage="SETTLED", owner_gate="APPROVED",
             source_uri="synthetic://source", evidence_uri="synthetic://evidence",
             revenue_mode="PRINCIPAL", review_state="REVIEWED",
             review_reference="synthetic://review", recognition_date="2026-11-02",
             settlement_date="2026-11-03", reported_revenue="200000",
             cash_collected="100000", direct_cost="120000", contract_estimate="200000")
    d.update(overrides)
    return d


class LedgerTests(unittest.TestCase):
    def test_approved_case_is_still_provisional(self):
        a = audit([row()])[0]
        self.assertEqual((a["revenue_gate"], a["cash_gate"]), ("REPORTING_PROVISIONAL", "CASH_REPORTING_PROVISIONAL"))
        self.assertFalse(a["accounting_verified"])
        self.assertEqual(a["provisional_cash"], "100000")

    def test_duplicated_case_blocks_both(self):
        x = audit([row(), row(case_id="syn-01")])
        self.assertTrue(all(v["revenue_gate"] == "DUPLICATE_ID" and v["provisional_revenue"] is None for v in x))

    def test_missing_id(self):
        self.assertEqual(audit([row(case_id=" ")])[0]["revenue_gate"], "MISSING_ID")

    def test_not_recognized(self):
        self.assertEqual(audit([row(stage="PROPOSAL_DRAFT")])[0]["revenue_gate"], "NOT_RECOGNIZED")

    def test_owner_gate(self):
        self.assertEqual(audit([row(owner_gate="CLOSED")])[0]["revenue_gate"], "OWNER_GATE_CLOSED")

    def test_evidence(self):
        self.assertEqual(audit([row(evidence_uri="")])[0]["revenue_gate"], "MISSING_SOURCE")

    def test_revenue_mode(self):
        self.assertEqual(audit([row(revenue_mode="MAYBE")])[0]["revenue_gate"], "MISSING_REVENUE_MODE")

    def test_review_state(self):
        self.assertEqual(audit([row(review_state="PENDING")])[0]["revenue_gate"], "REVIEW_PENDING")

    def test_review_reference(self):
        self.assertEqual(audit([row(review_reference="")])[0]["revenue_gate"], "MISSING_REVIEW_REFERENCE")

    def test_recognition_date_invalid(self):
        self.assertEqual(audit([row(recognition_date="2026-02-30")])[0]["revenue_gate"], "RECOGNITION_DATE_MISSING")

    def test_revenue_invalid(self):
        for bad in (None, "", -1, "NaN", "Infinity", True):
            with self.subTest(bad=bad):
                self.assertEqual(audit([row(reported_revenue=bad)])[0]["revenue_gate"], "INVALID_REVENUE")

    def test_cost_unknown_not_zero(self):
        self.assertEqual(audit([row(direct_cost="")])[0]["revenue_gate"], "DIRECT_COST_UNKNOWN")

    def test_agent_gmv_cannot_be_revenue(self):
        good = audit([row(revenue_mode="AGENT",contract_estimate="40000",reported_revenue="3200")])[0]
        self.assertEqual(good["provisional_revenue"], "3200")
        bad = audit([row(revenue_mode="AGENT",contract_estimate="1000",reported_revenue="3200")])[0]
        self.assertEqual(bad["revenue_gate"], "AGENT_GMV_RISK")

    def test_settlement_date_missing(self):
        self.assertEqual(audit([row(settlement_date="")])[0]["cash_gate"], "SETTLEMENT_DATE_MISSING")

    def test_cash_missing_not_zero(self):
        a = audit([row(cash_collected="")])[0]
        self.assertEqual(a["revenue_gate"], "REPORTING_PROVISIONAL")
        self.assertEqual(a["cash_gate"], "CASH_UNKNOWN_OR_INVALID")
        self.assertIsNone(a["provisional_cash"])

    def test_recognized_not_paid(self):
        a = audit([row(stage="RECOGNIZED",cash_collected=None)])[0]
        self.assertEqual(a["revenue_gate"], "REPORTING_PROVISIONAL")
        self.assertEqual(a["cash_gate"], "NOT_SETTLED")

    def test_invalid_row(self):
        self.assertEqual(audit([None])[0]["revenue_gate"], "INVALID_ROW")

    def test_empty_list_is_unknown_not_zero(self):
        self.assertEqual(audit([]), [])

    def test_list_required(self):
        with self.assertRaises(ValueError):
            audit({})


if __name__ == "__main__":
    unittest.main()
