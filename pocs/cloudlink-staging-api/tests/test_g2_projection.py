import unittest
from g2_projection import ContractBlocked, ReviewProjection, staging_to_review_projection, assert_live_sync_enabled

OK = dict(id="mock-case-1", category="cctv", region="台南市", description="虛構 CCTV 安裝需求僅供隔離測試。", state="APPROVED")
EV = dict(consent_evidence_ref="evidence:consent-1", moderation_evidence_ref="evidence:review-1")

class TestG2Projection(unittest.TestCase):
    def test_cctv_projection_is_review_only(self):
        out = staging_to_review_projection(OK, **EV)
        self.assertEqual((out.service_code, out.region_code, out.state), ("CCTV", "TNN", "REVIEW_ONLY"))
        self.assertFalse(out.executable)

    def test_wifi_and_tai_variant(self):
        out = staging_to_review_projection({**OK,"category":"network", "region":"臺南市"}, **EV)
        self.assertEqual(out.service_code,"WIFI")

    def test_nas_not_auto_enabled(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection({**OK,"category":"nas"}, **EV)

    def test_legacy_access_not_pilot(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection({**OK,"category":"access"}, **EV)

    def test_other_region_needs_coverage(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection({**OK,"region":"高雄市"}, **EV)

    def test_unapproved_not_allowed(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection({**OK,"state":"PENDING"}, **EV)

    def test_consent_evidence_required(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection(OK, **{**EV,"consent_evidence_ref":""})

    def test_moderation_evidence_required(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection(OK, **{**EV,"moderation_evidence_ref":"missing"})

    def test_missing_id_denied(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection({**OK, "id": ""}, **EV)

    def test_short_description_denied(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection({**OK, "description": "short"}, **EV)

    def test_live_sync_never_enabled(self):
        with self.assertRaisesRegex(ContractBlocked, "not connected"):
            assert_live_sync_enabled(identity_verified=True, tenant_rbac_verified=True,
                 audit_write_verified=True, owner_authorized=True)

    def test_invalid_shape_denied(self):
        with self.assertRaises(ContractBlocked):
            staging_to_review_projection([], **EV)

if __name__ == "__main__":
    unittest.main()
