"""2026-11-02 CCTV synthetic case policy gate; no network, secrets, money or real customer data."""
import unittest

from marketplace_contract import (
    CustomerRequest, Contractor, PortfolioCase,
    eligible_contractors, estimate_service_fee,
    may_mark_service_fee_reconciled, may_publish_case,
)
from g2_projection import ContractBlocked, assert_live_sync_enabled, staging_to_review_projection


class TestTbmCctvSyntheticGate(unittest.TestCase):
    def test_one_cctv_case_reaches_review_only_not_commercial_acceptance(self):
        case_id = "CCTV-SYNTHETIC-20261102-001"
        draft = CustomerRequest("cctv", "台南市", False, False, "DRAFT")
        approved = CustomerRequest("cctv", "台南市", True, True, "APPROVED")
        contractors = [
            Contractor("synthetic-qualified-TNN", ("cctv",), ("台南市",), True, True),
            Contractor("synthetic-unverified-TNN", ("cctv",), ("台南市",), False, True),
            Contractor("synthetic-out-of-region", ("cctv",), ("高雄市",), True, True),
        ]
        self.assertEqual(eligible_contractors(draft, contractors), [])
        self.assertEqual(eligible_contractors(approved, contractors), ["synthetic-qualified-TNN"])

        row = {
            "id": case_id,
            "category": "cctv",
            "region": "台南市",
            "description": "虛構商家 4 支監視器影像錄製與佈線調整，不含現場資料或個資。",
            "state": "APPROVED",
        }
        view = staging_to_review_projection(
            row,
            consent_evidence_ref="evidence:synthetic-consent-stub",
            moderation_evidence_ref="evidence:synthetic-moderation-stub",
        )
        self.assertEqual((view.source_request_id, view.service_code, view.region_code),
                         (case_id, "CCTV", "TNN"))
        self.assertEqual((view.state, view.executable), ("REVIEW_ONLY", False))
        with self.assertRaisesRegex(ContractBlocked, "runtime is not connected"):
            assert_live_sync_enabled(identity_verified=True, tenant_rbac_verified=True,
                                     audit_write_verified=True, owner_authorized=True)

        # Quote and selection are narrative-only synthetic checkpoints here, NOT live app calls.
        synthetic_quote = {"contractor": "synthetic-qualified-TNN", "price_ntd": "18000",
                           "scope": "4 支 CCTV 模擬設備／施工／保固欄位；非正式報價"}
        self.assertEqual(synthetic_quote["contractor"], eligible_contractors(approved, contractors)[0])
        self.assertGreater(int(synthetic_quote["price_ntd"]), 0)
        with self.assertRaisesRegex(ValueError, "Contract and Owner approval"):
            estimate_service_fee(synthetic_quote["price_ntd"], "5", contract_accepted=False, owner_approved=False)
        self.assertFalse(may_mark_service_fee_reconciled(
            owner_approved=False, invoice_verified=False,
            bank_reconciliation_verified=False, contract_accepted=False))
        self.assertFalse(may_publish_case(PortfolioCase(False, False, True, False)))

    def test_negative_policy_cases_fail_closed(self):
        base = {"id": "SYNTH-NEGATIVE-1", "category": "cctv", "region": "台南市",
                "state": "APPROVED", "description": "合成影像監控需求，僅限測試資料使用。"}
        kwargs = {"consent_evidence_ref": "evidence:synthetic-consent-stub",
                  "moderation_evidence_ref": "evidence:synthetic-review-stub"}
        for altered in ({"category": "nas"}, {"region": "高雄市"}, {"state": "PENDING"}):
            with self.subTest(altered=altered), self.assertRaises(ContractBlocked):
                staging_to_review_projection({**base, **altered}, **kwargs)
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection(base, **{**kwargs, "consent_evidence_ref": ""})
        self.assertFalse(may_mark_service_fee_reconciled(
            owner_approved=True, invoice_verified=False,
            bank_reconciliation_verified=True, contract_accepted=True))


if __name__ == "__main__":
    unittest.main()
