"""Offline, read-only projection contract; NOT a Business OS adapter or IAM boundary.

Fail closed until consent and moderation evidence are separately verified.
No persistence, external requests, approval, publication, or money movement.
"""
from dataclasses import dataclass

class ContractBlocked(ValueError):
    pass

@dataclass(frozen=True)
class ReviewProjection:
    source_request_id: str
    service_code: str
    region_code: str
    description: str
    consent_evidence_ref: str
    moderation_evidence_ref: str
    state: str = "REVIEW_ONLY"
    executable: bool = False

# First pilot: CCTV & Wi-Fi in Tainan only. NAS is waiting for API support.
_CATEGORY = {"cctv": "CCTV", "network": "WIFI"}
_TAINAN = {"台南市", "臺南市"}


def staging_to_review_projection(staging_row: dict, *, consent_evidence_ref: str,
                                 moderation_evidence_ref: str) -> ReviewProjection:
    if not isinstance(staging_row, dict):
        raise ContractBlocked("invalid staging record")
    rid = staging_row.get("id")
    category = staging_row.get("category")
    region = staging_row.get("region")
    desc = staging_row.get("description")
    if staging_row.get("state") != "APPROVED":
        raise ContractBlocked("moderation state is not approved")
    if category not in _CATEGORY:
        raise ContractBlocked("category not supported in G2 pilot")
    if region not in _TAINAN:
        raise ContractBlocked("region needs separate approved coverage")
    if not isinstance(rid, str) or not rid.strip():
        raise ContractBlocked("missing source request ID")
    if not isinstance(desc, str) or len(desc.strip()) < 12:
        raise ContractBlocked("invalid demand description")
    for ref in (consent_evidence_ref, moderation_evidence_ref):
        if not isinstance(ref, str) or not ref.startswith("evidence:") or len(ref) < 15:
            raise ContractBlocked("independent evidence reference required")
    return ReviewProjection(rid, _CATEGORY[category], "TNN", desc,
                            consent_evidence_ref, moderation_evidence_ref)


def assert_live_sync_enabled(*, identity_verified: bool = False,
                             tenant_rbac_verified: bool = False,
                             audit_write_verified: bool = False,
                             owner_authorized: bool = False) -> None:
    """No live Business OS sync is implemented, regardless of caller flags."""
    raise ContractBlocked("Business OS runtime is not connected; no live synchronization")
