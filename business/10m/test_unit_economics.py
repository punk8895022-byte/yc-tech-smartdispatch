"""Run: python -m unittest discover -s business/10m -p 'test_unit_economics.py' -v"""
import unittest
from unit_economics import evaluate


def principal(**changes):
    case = dict(case_id="SYNTH-PRINCIPAL", stage="SETTLED", owner_gate="APPROVED",
                evidence_uri="synthetic://not-a-real-order", revenue_mode="PRINCIPAL",
                reported_revenue="200000", gmv="200000", direct_cost="120000",
                cac="10000", variable_support="5000")
    case.update(changes)
    return case


class UnitEconomicsTests(unittest.TestCase):
    def test_principal_example(self):
        out = evaluate(principal())
        self.assertEqual(out["contribution"], "65000")
        self.assertEqual(out["contribution_margin"], "0.325")
        self.assertEqual(out["status"], "CALCULABLE_UNVERIFIED")

    def test_agent_fee_not_gmv(self):
        out = evaluate(principal(case_id="SYNTH-AGENT", revenue_mode="AGENT",
                                 gmv="40000", reported_revenue="3200",
                                 direct_cost="1000", cac="300", variable_support="200"))
        self.assertEqual(out["contribution"], "1700")
        self.assertEqual(out["contribution_margin"], "0.53125")

    def test_missing_owner_approval(self):
        self.assertEqual(evaluate(principal(owner_gate="CLOSED"))["status"], "OWNER_GATE_CLOSED")

    def test_no_evidence(self):
        self.assertEqual(evaluate(principal(evidence_uri=""))["status"], "MISSING_EVIDENCE")

    def test_draft_does_not_count(self):
        self.assertEqual(evaluate(principal(stage="PROPOSAL_DRAFT"))["status"], "NOT_RECOGNIZED")

    def test_blank_cost_unknown_not_zero(self):
        self.assertEqual(evaluate(principal(cac=""))["status"], "MISSING_COST_OR_INVALID")

    def test_invalid_amount_rejected(self):
        for bad in ("-1", "NaN", "Infinity", "not-money", None, True):
            with self.subTest(bad=bad):
                self.assertEqual(evaluate(principal(direct_cost=bad))["status"], "MISSING_COST_OR_INVALID")

    def test_agent_fee_above_gmv_rejected(self):
        self.assertEqual(evaluate(principal(revenue_mode="AGENT", gmv="500", reported_revenue="1000"))["status"], "AGENT_GMV_CHECK")

    def test_unknown_cash_remains_unknown(self):
        self.assertIsNone(evaluate(principal())["cash_collected"])
        self.assertEqual(evaluate(principal(cash_collected="0"))["cash_collected"], "0")

    def test_cash_does_not_change_recognized_revenue(self):
        a = evaluate(principal(cash_collected="0"))
        b = evaluate(principal(cash_collected="999999"))
        self.assertEqual(a["contribution"], b["contribution"])

    def test_zero_revenue_margin_unknown(self):
        self.assertIsNone(evaluate(principal(reported_revenue="0"))["contribution_margin"])

    def test_missing_id(self):
        self.assertEqual(evaluate(principal(case_id=""))["status"], "MISSING_ID")


if __name__ == "__main__":
    unittest.main()
