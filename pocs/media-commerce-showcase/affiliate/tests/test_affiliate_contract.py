"""Offline, no-dependency affiliate sandbox contract tests; not browser/real affiliate E2E."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/"offers.json").read_text(encoding="utf-8"))
        cls.html=(ROOT/"index.html").read_text(encoding="utf-8")
        cls.js=(ROOT/"sandbox.js").read_text(encoding="utf-8")
    def test_three_unique_subids(self):
        self.assertEqual(len(self.manifest["offers"]),3)
        self.assertEqual(len({v["subid"] for v in self.manifest["offers"]}),3)
    def test_all_destinations_blocked(self):
        self.assertTrue(all(not v["destination"] for v in self.manifest["offers"]))
        self.assertTrue(all(v["status"]=="SYNTHETIC_NOT_APPROVED" for v in self.manifest["offers"]))
    def test_non_public_owner_gate(self):
        self.assertEqual(self.manifest["owner_gate"],"CLOSED")
        self.assertFalse(self.manifest["real_tracking_enabled"])
        self.assertFalse(self.manifest["real_payouts_enabled"])
        self.assertIn('noindex,nofollow,noarchive',self.html)
    def test_no_outbound_network_or_storage(self):
        for forbidden in ("fetch(","XMLHttpRequest","sendBeacon","localStorage","sessionStorage","document.cookie","https://","http://"):
            self.assertNotIn(forbidden,self.js)
    def test_explicit_disclosure_and_real_zero(self):
        self.assertIn("商業揭露",self.html)
        self.assertIn("真實已結算",self.js)
        self.assertIn("money(0)",self.js)
    def test_all_subids_rendered(self):
        for v in self.manifest["offers"]:
            self.assertIn(v["subid"],self.html)
            self.assertIn(v["subid"],self.js)
if __name__=="__main__":unittest.main()
