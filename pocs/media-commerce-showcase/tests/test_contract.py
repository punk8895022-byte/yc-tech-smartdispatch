"""Media Commerce showcase: offline, stdlib-only contract checks. Not a browser E2E."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "xy-hd-001.html", "cloudlink.html")


class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.hrefs = []
        self.tags = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        info = dict(attrs)
        self.tags.append(tag)
        self.attrs.append((tag, info))
        if "id" in info:
            self.ids.add(info["id"])
        if tag in ("a", "link") and "href" in info:
            self.hrefs.append(info["href"])


class ShowcaseContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {name: (ROOT / name).read_text(encoding="utf-8") for name in PAGES}
        cls.parsed = {}
        for name, html in cls.pages.items():
            p = Tags()
            p.feed(html)
            cls.parsed[name] = p
        cls.manifest = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))

    def test_01_exactly_two_listed_projects(self):
        self.assertEqual(len(self.manifest["projects"]), 2)
        self.assertEqual([x["id"] for x in self.manifest["projects"]], ["XY-HD-001", "CLOUDLINK-M1B"])

    def test_02_all_pages_have_mobile_viewport(self):
        for name, html in self.pages.items():
            with self.subTest(name=name):
                self.assertIn('name="viewport"', html)

    def test_03_all_pages_are_nonindexed(self):
        for name, html in self.pages.items():
            with self.subTest(name=name):
                self.assertIn('content="noindex,nofollow,noarchive"', html)

    def test_04_owner_gate_fails_closed(self):
        self.assertEqual(self.manifest["publishing"]["owner_gate"], "CLOSED")
        for key in ("public_approved", "payment_enabled", "forms_enabled", "tracking_enabled"):
            self.assertIs(self.manifest["publishing"][key], False)
        self.assertTrue(all(x["public_approved"] is False for x in self.manifest["projects"]))

    def test_05_all_showcase_routes_are_real_files(self):
        for project in self.manifest["projects"]:
            self.assertTrue((ROOT / project["route"]).is_file())

    def test_06_no_forms_scripts_or_embedded_third_party(self):
        for name, parsed in self.parsed.items():
            with self.subTest(name=name):
                self.assertNotIn("form", parsed.tags)
                self.assertNotIn("script", parsed.tags)
                self.assertNotIn("iframe", parsed.tags)
                self.assertNotIn("input", parsed.tags)
                self.assertNotIn("img", parsed.tags)

    def test_07_all_internal_link_targets_exist(self):
        for name, parsed in self.parsed.items():
            for href in parsed.hrefs:
                with self.subTest(page=name, href=href):
                    parts = urlsplit(href)
                    self.assertFalse(parts.scheme or parts.netloc, "external resource not allowed")
                    target = (ROOT / unquote(parts.path)).resolve() if parts.path else ROOT / name
                    self.assertTrue(target.is_file(), f"missing target: {target}")
                    if parts.fragment and target.name in self.pages:
                        self.assertIn(parts.fragment, self.parsed[target.name].ids)

    def test_08_home_has_both_project_links(self):
        html = self.pages["index.html"]
        for name in ("xy-hd-001.html", "cloudlink.html"):
            self.assertIn(f'href="./{name}"', html)

    def test_09_both_detail_pages_have_evidence_and_limits(self):
        for name in PAGES[1:]:
            html = self.pages[name]
            with self.subTest(name=name):
                self.assertIn('id="evidence"', html)
                self.assertIn("合成", html)
                self.assertRegex(html, r"NOT_RUN|NOT_VERIFIED|BLOCKED")

    def test_10_mobile_breakpoints_and_focus_visible(self):
        css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("@media(max-width:390px)", css)
        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_11_no_trackers_secrets_or_payment_forms(self):
        combined = "\n".join(self.pages.values())
        for forbidden in ("GEMINI_API_KEY=", "sk-", "token=", "Stripe(", "gtag(", "fbq(", "fetch(", "localStorage"):
            self.assertNotIn(forbidden, combined)
        self.assertFalse(re.search(r'https?://', combined))

    def test_12_all_pages_have_main_and_skip_link(self):
        for name, p in self.parsed.items():
            with self.subTest(name=name):
                self.assertIn("main", p.tags)
                self.assertIn("main", p.ids)
                self.assertIn("#main", p.hrefs)

    def test_13_evidence_is_scoped_not_runtime_verified(self):
        for project in self.manifest["projects"]:
            self.assertEqual(project["demo_kind"], "STATIC_SYNTHETIC")
            self.assertEqual(project["evidence_status"], "EXISTING_SOURCE_CITED_NOT_RETESTED")
            self.assertTrue(project["limitations"])

    def test_14_no_public_launch_language(self):
        for name, html in self.pages.items():
            with self.subTest(name=name):
                self.assertIn("INTERNAL REVIEW", html)
                self.assertTrue("未" in html or "CLOSED" in html)


if __name__ == "__main__":
    unittest.main()
