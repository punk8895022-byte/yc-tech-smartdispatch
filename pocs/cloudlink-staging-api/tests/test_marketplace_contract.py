"""Synthetic offline tests only; no database, network, or actual customer data."""
import unittest
from marketplace_contract import (
    PortfolioCase, CustomerRequest, Contractor, may_publish_case,
    eligible_contractors, estimate_service_fee, may_mark_service_fee_reconciled,
)

class MarketplaceContractTests(unittest.TestCase):
    def test_case_publish_all_gates(self):
        self.assertTrue(may_publish_case(PortfolioCase(True, True, True, True)))

    def test_case_publish_any_missing_gate(self):
        for i in range(4):
            gates = [True] * 4
            gates[i] = False
            self.assertFalse(may_publish_case(PortfolioCase(*gates)))

    def test_no_match_before_customer_consent(self):
        self.assertEqual(eligible_contractors(self.request(consent=False), [self.worker()]), [])

    def test_no_match_before_moderation(self):
        self.assertEqual(eligible_contractors(self.request(moderation=False), [self.worker()]), [])

    def test_no_match_for_draft(self):
        self.assertEqual(eligible_contractors(self.request(status="DRAFT"), [self.worker()]), [])

    def test_only_qualified_approved_active_region_skill(self):
        pool = [self.worker(), self.worker(id="no_skill", skills=("NAS",)),
                self.worker(id="wrong_region", regions=("臺北",)),
                self.worker(id="unverified", qualified=False),
                self.worker(id="unapproved", approved=False),
                self.worker(id="inactive", active=False)]
        self.assertEqual(eligible_contractors(self.request(), pool), ["approved"])

    def test_fee_requires_owner_and_accepted_contract(self):
        for accepted, approved in [(True, False), (False, True), (False, False)]:
            with self.assertRaises(ValueError):
                estimate_service_fee("10000", "5", contract_accepted=accepted,
                                     owner_approved=approved)

    def test_fee_is_only_integer_estimate(self):
        self.assertEqual(str(estimate_service_fee("10101", "5.5",
                         contract_accepted=True, owner_approved=True)), "556")

    def test_fee_rejects_invalid_or_nonfinite(self):
        for amount, rate in [("0", "5"), ("-1", "5"), ("NaN", "5"),
                             ("100", "Infinity"), ("100", "-1"), ("100", "101"),
                             ("garbage", "5")]:
            with self.assertRaises(ValueError):
                estimate_service_fee(amount, rate, contract_accepted=True,
                                     owner_approved=True)

    def test_reconciliation_requires_all_evidence(self):
        self.assertTrue(may_mark_service_fee_reconciled(owner_approved=True,
            invoice_verified=True, bank_reconciliation_verified=True,
            contract_accepted=True))
        for key in ("owner_approved", "invoice_verified", "bank_reconciliation_verified", "contract_accepted"):
            data = dict.fromkeys(("owner_approved", "invoice_verified",
                     "bank_reconciliation_verified", "contract_accepted"), True)
            data[key] = False
            self.assertFalse(may_mark_service_fee_reconciled(**data))

    @staticmethod
    def request(*, consent=True, moderation=True, status="APPROVED"):
        return CustomerRequest("CCTV", "臺南", consent, moderation, status)

    @staticmethod
    def worker(*, id="approved", skills=("CCTV",), regions=("臺南",),
               qualified=True, approved=True, active=True):
        return Contractor(id, skills, regions, qualified, approved, active)

if __name__ == "__main__":
    unittest.main()
