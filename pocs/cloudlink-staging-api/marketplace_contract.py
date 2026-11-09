"""Offline YC Tech Match G1 contracts; no storage, network, payments, or public APIs.

This module is a staging-only policy seam. Production permissions MUST be enforced
by Business OS server-side authorization and audited application services.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


@dataclass(frozen=True)
class PortfolioCase:
    rights_cleared: bool
    client_permission: bool
    pii_redacted: bool
    owner_approved: bool


def may_publish_case(case: PortfolioCase) -> bool:
    """Publication gate: no public case without ALL four approvals."""
    return all((case.rights_cleared, case.client_permission,
                case.pii_redacted, case.owner_approved))


@dataclass(frozen=True)
class CustomerRequest:
    skill: str
    region: str
    customer_consented: bool
    moderation_approved: bool
    status: str = "DRAFT"


@dataclass(frozen=True)
class Contractor:
    identifier: str
    skills: tuple[str, ...]
    service_regions: tuple[str, ...]
    qualification_checked: bool
    owner_approved: bool
    active: bool = True


def eligible_contractors(request: CustomerRequest, contractors: list[Contractor]) -> list[str]:
    """Returns approved IDs, never exposes contact details or an automatic bid."""
    if not (request.customer_consented and request.moderation_approved
            and request.status == "APPROVED" and request.skill and request.region):
        return []
    return [c.identifier for c in contractors if c.active and c.qualification_checked
            and c.owner_approved and request.skill in c.skills
            and request.region in c.service_regions]


def estimate_service_fee(contract_total: str, fee_percent: str, *,
                         contract_accepted: bool, owner_approved: bool) -> Decimal:
    """Nonbinding fee estimate; does NOT create a charge, ledger or settlement."""
    if not (contract_accepted and owner_approved):
        raise ValueError("Contract and Owner approval required")
    try:
        amount = Decimal(contract_total)
        percent = Decimal(fee_percent)
    except (InvalidOperation, TypeError) as exc:
        raise ValueError("Invalid financial input") from exc
    if not (amount.is_finite() and percent.is_finite() and amount > 0
            and Decimal("0") <= percent <= Decimal("100")):
        raise ValueError("Invalid amount or fee percentage")
    return (amount * percent / Decimal("100")).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)


def may_mark_service_fee_reconciled(*, owner_approved: bool,
                                    invoice_verified: bool,
                                    bank_reconciliation_verified: bool,
                                    contract_accepted: bool) -> bool:
    """Strict evidence gate; never mutates finance state."""
    return all((owner_approved, invoice_verified,
                bank_reconciliation_verified, contract_accepted))
