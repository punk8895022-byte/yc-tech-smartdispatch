#!/usr/bin/env python3
"""Fail-closed editorial intake for Media Commerce static showcase.

This tool DOES NOT authenticate Owner approval, post to third-party platforms,
produce a deployable site, or claim real product E2E. Python stdlib only.
"""
import argparse
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "projects.json"
ALLOWED_STATUS = {"INTERNAL_PREVIEW"}
ALLOWED_DEMO = {"STATIC_SYNTHETIC"}


def load(path=MANIFEST):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_internal(m, root=ROOT):
    errors = []
    if not isinstance(m, dict):
        return ["manifest must be a JSON object"]
    if m.get("scope") != "INTERNAL_PREVIEW_ONLY":
        errors.append("scope must stay INTERNAL_PREVIEW_ONLY")
    publish = m.get("publishing", {})
    if publish.get("owner_gate") != "CLOSED":
        errors.append("Owner gate must stay CLOSED")
    for flag in ("public_approved", "payment_enabled", "forms_enabled", "tracking_enabled"):
        if publish.get(flag) is not False:
            errors.append(f"publishing.{flag} must be false")
    dist = m.get("distribution", {})
    if dist.get("external_posting") != "DISABLED":
        errors.append("external posting must be DISABLED")
    if dist.get("public_tracking") != "DISABLED":
        errors.append("public tracking must be DISABLED")
    if dist.get("submissions") != []:
        errors.append("no external submissions may be recorded as posted")
    if m.get("discovery", {}).get("public_likes") is not False:
        errors.append("no fictional like counts")
    if m.get("discovery", {}).get("public_sorting") is not False:
        errors.append("no unverified popularity sorting")
    projects = m.get("projects")
    if not isinstance(projects, list) or len(projects) != 2:
        return errors + ["exactly two projects required in this MVP"]
    ids, routes = set(), set()
    category_ids = {
        c.get("id") for c in m.get("discovery", {}).get("categories", [])
        if isinstance(c, dict) and isinstance(c.get("id"), str)
    }
    for i, p in enumerate(projects):
        tag = f"project[{i}]"
        if not isinstance(p, dict):
            errors.append(tag + " must be object")
            continue
        pid, route = p.get("id"), p.get("route")
        if not isinstance(pid, str) or not pid.strip() or pid in ids:
            errors.append(tag + " missing/duplicate id")
        else:
            ids.add(pid)
        if not isinstance(route, str):
            errors.append(tag + " route missing")
        else:
            segment = PurePosixPath(route)
            if (segment.is_absolute() or len(segment.parts) != 1 or
                    segment.suffix != ".html" or route in routes):
                errors.append(tag + " route must be one unique flat html file")
            else:
                routes.add(route)
                if not (Path(root) / route).is_file():
                    errors.append(tag + " route file missing")
        if p.get("category") not in category_ids:
            errors.append(tag + " category not in discovery catalog")
        if p.get("public_approved") is not False:
            errors.append(tag + " public_approved must be false")
        if p.get("display_status") not in ALLOWED_STATUS:
            errors.append(tag + " cannot claim public live state")
        if p.get("demo_kind") not in ALLOWED_DEMO:
            errors.append(tag + " demo must be marked synthetic")
        if p.get("evidence_status") != "EXISTING_SOURCE_CITED_NOT_RETESTED":
            errors.append(tag + " evidence must not claim newly run product E2E")
        if p.get("external_submission_status") != "NOT_SUBMITTED":
            errors.append(tag + " must not claim external submission")
        if not isinstance(p.get("limitations"), list) or not p["limitations"]:
            errors.append(tag + " must disclose limitations")
        pos = p.get("positioning")
        if not isinstance(pos, dict) or not all(
            isinstance(pos.get(k), str) and pos[k].strip()
            for k in ("problem", "audience", "proof_statement")
        ):
            errors.append(tag + " positioning must describe problem/audience/proof")
        reviews = p.get("review_requirements", {})
        for k, expected in (
            ("rights", "HOLD"), ("pii", "REVIEW_PENDING"),
            ("product_e2e", "NOT_VERIFIED"), ("owner", "NOT_APPROVED")
        ):
            if reviews.get(k) != expected:
                errors.append(tag + " review must stay blocked: " + k)
    return errors


def public_blockers(m):
    """Advisory only; never constitutes approval or authorization."""
    blocked = ["OWNER_SIGNOFF_MUST_BE_VERIFIED_OUTSIDE_THIS_SCRIPT"]
    publishing = m.get("publishing", {})
    if publishing.get("owner_gate") != "APPROVED":
        blocked.append("OWNER_GATE_CLOSED")
    if publishing.get("public_approved") is not True:
        blocked.append("PUBLIC_RELEASE_NOT_APPROVED")
    for p in m.get("projects", []):
        if p.get("public_approved") is not True:
            blocked.append(p.get("id", "UNKNOWN") + ":PUBLIC_NOT_APPROVED")
        for key, status in p.get("review_requirements", {}).items():
            if status != "APPROVED":
                blocked.append(p.get("id", "UNKNOWN") + ":" + key.upper() + "_NOT_APPROVED")
    return blocked


def review_packet(m):
    """Generate internal reviewer notes only; deliberately no publish API/URL."""
    lines = [
        "# 小雲 Media Commerce｜作品探索審核稿（不對外發布）",
        "",
        "狀態：INTERNAL ONLY / OWNER GATE CLOSED / NOT SUBMITTED",
        "資料來源：projects.json；權威仍在既有 Business OS / Asset OS。",
        "注意：沒有真實 Like、評論、排行、客戶詢問或營收數據。",
        "",
    ]
    for p in m["projects"]:
        pos = p["positioning"]
        lines.extend([
            "## " + p["id"] + "｜" + p["name"],
            "- 目標族群：" + pos["audience"],
            "- 使用痛點：" + pos["problem"],
            "- 已知證據及範圍：" + pos["proof_statement"],
            "- Demo：" + p["demo_kind"],
            "- 可公開狀態：未核准；" + p["external_submission_status"],
            "- 阻塞：" + "、".join(p["limitations"]),
            "",
        ])
    lines.append("下一步：獨立 Reviewer 驗證授權、個資、真實 Demo 與適用平台規則；Owner 核准前不投稿。")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Offline showcase editorial gate; never deploys")
    parser.add_argument("--mode", choices=("internal", "public", "packet"), default="internal")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    m = load(args.manifest)
    internal_errors = validate_internal(m, args.manifest.resolve().parent)
    if args.mode in ("internal", "packet") and internal_errors:
        for error in internal_errors:
            print("BLOCKED:", error)
        return 2
    if args.mode == "internal":
        print("INTERNAL_SHOWCASE_PREFLIGHT_PASS; PUBLIC_RELEASE_CLOSED")
        return 0
    if args.mode == "packet":
        print(review_packet(m))
        return 0
    for error in public_blockers(m):
        print("PUBLIC_RELEASE_BLOCKED:", error)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
