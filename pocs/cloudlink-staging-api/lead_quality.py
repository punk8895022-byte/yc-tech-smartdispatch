"""Read-only evidence-card ranking inspired by TBM public UX, not TBM software.

NO network, scraping, login, PII persistence, identity verification, bidding,
publication, Business OS sync, finance, or production authorization.
Scores express **metadata completeness and local service fit**, not authenticity,
chance of winning, customer consent, contractor qualification, or approval.
"""
from dataclasses import dataclass
from datetime import date
from ipaddress import ip_address
import re
from urllib.parse import urlsplit


class LeadInputError(ValueError):
    """An untrusted lead card is not safe or sufficient to evaluate."""


@dataclass(frozen=True)
class LeadAssessment:
    source_host: str
    source_mode: str
    score: int
    review_state: str
    reason_codes: tuple[str, ...]
    executable: bool = False
    can_contact: bool = False
    can_bid: bool = False
    can_publish: bool = False
    can_sync: bool = False
    financial_status: str = "NOT_AVAILABLE"


_KEYS = frozenset({"source_mode", "source_url", "observed_on", "posted_on",
                   "category", "region", "scope_confirmed", "budget_known", "deadline_known"})
_SCOPED_CATEGORIES = {"cctv", "network"}
_SCOPED_REGIONS = {"台南市", "臺南市"}


def _public_source_host(url: str) -> str:
    if not isinstance(url, str) or not 9 <= len(url) <= 1200:
        raise LeadInputError("source url missing/invalid")
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower().rstrip(".")
        port = parts.port
    except ValueError as exc:
        raise LeadInputError("invalid source URL") from exc
    if (parts.scheme != "https" or not host or parts.username is not None or
        parts.password is not None or parts.query or parts.fragment or port not in (None, 443)):
        raise LeadInputError("source must be public HTTPS without credentials or query tokens")
    if not re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", host):
        raise LeadInputError("source host invalid")
    if host.endswith((".invalid", ".local", ".localhost", ".internal", ".test", ".example")):
        raise LeadInputError("non-public source host")
    try:
        ip_address(host)
    except ValueError:
        pass
    else:
        raise LeadInputError("IP-literal sources not accepted")
    return host


def _date(value, *, allow_none: bool) -> date | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise LeadInputError("date must use YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise LeadInputError("invalid source date") from exc


def evaluate_public_lead(card: dict, *, as_of: date) -> LeadAssessment:
    """Classify *manually transcribed* public metadata or synthetic fixture.

    A 100/100 score does NOT approve any contact, bid, publication, or data sync.
    No raw description or contact data may enter this function; unknown fields fail.
    """
    if not isinstance(card, dict) or set(card) != _KEYS:
        raise LeadInputError("exact metadata-only fields required; PII not accepted")
    if not isinstance(as_of, date) or isinstance(as_of, type(None)):
        raise LeadInputError("as_of must be a date")
    mode = card["source_mode"]
    if mode not in ("PUBLIC_MANUAL", "SYNTHETIC") or not isinstance(mode, str):
        raise LeadInputError("only manual public metadata or synthetic fixtures allowed")
    host = _public_source_host(card["source_url"])
    observed = _date(card["observed_on"], allow_none=False)
    posted = _date(card["posted_on"], allow_none=True)
    if observed > as_of or (posted is not None and (posted > observed or posted > as_of)):
        raise LeadInputError("inconsistent or future source dates")
    if not isinstance(card["category"], str) or not isinstance(card["region"], str):
        raise LeadInputError("category and region must be text")
    for key in ("scope_confirmed", "budget_known", "deadline_known"):
        if type(card[key]) is not bool:
            raise LeadInputError(f"{key} must be explicit boolean")

    reasons = ["IDENTITY_AND_CONSENT_NOT_VERIFIED", "PUBLIC_ACCESS_AND_RIGHTS_NOT_VERIFIED"]
    if mode == "SYNTHETIC":
        reasons.append("SYNTHETIC_NONCOMMERCIAL")
    if card["category"] not in _SCOPED_CATEGORIES:
        reasons.append("OUT_OF_SCOPE_CATEGORY")
    if card["region"] not in _SCOPED_REGIONS:
        reasons.append("OUT_OF_SERVICE_REGION")
    if card["category"] not in _SCOPED_CATEGORIES or card["region"] not in _SCOPED_REGIONS:
        return LeadAssessment(host, mode, 0, "OUT_OF_SCOPE", tuple(reasons))

    score = 50  # category + regional fit; not proof of validity
    if card["scope_confirmed"]:
        score += 20
    else:
        reasons.append("SCOPE_UNCONFIRMED")
    if card["budget_known"]:
        score += 10
    else:
        reasons.append("BUDGET_UNKNOWN")
    if card["deadline_known"]:
        score += 5
    else:
        reasons.append("DEADLINE_UNKNOWN")
    if posted is None:
        reasons.append("POSTED_DATE_UNKNOWN")
    else:
        age = (as_of - posted).days
        if age <= 7:
            score += 15
        elif age <= 30:
            score += 8
        else:
            reasons.append("STALE_OVER_30_DAYS")
    ready = (mode == "PUBLIC_MANUAL" and posted is not None and
             (as_of - posted).days <= 30 and card["scope_confirmed"] and
             card["budget_known"] and card["deadline_known"])
    return LeadAssessment(host, mode, score, "REVIEW_CANDIDATE" if ready else "NEEDS_EVIDENCE", tuple(reasons))
