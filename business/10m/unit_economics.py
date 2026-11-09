"""Offline 10M contribution checker; never writes ledger or recognizes revenue.

All values must be user-supplied and supported by independently reviewed evidence.
Use the main 10M sheet as the authoritative ledger, not this tool.
"""
from decimal import Decimal, InvalidOperation
import json
import sys

MONEY_FIELDS = ("reported_revenue", "direct_cost", "cac", "variable_support")


def _money(value):
    if value is None or value == "" or isinstance(value, bool):
        raise ValueError("missing monetary input")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid monetary input") from exc
    if not number.is_finite() or number < 0:
        raise ValueError("nonfinite or negative monetary input")
    return number


def evaluate(case):
    """Returns a guarded estimate; CALCULABLE_UNVERIFIED is NOT finance approval."""
    def blocked(reason):
        return {"case_id": case.get("case_id"), "status": reason,
                "contribution": None, "contribution_margin": None,
                "cash_collected": None}

    if not str(case.get("case_id") or "").strip():
        return blocked("MISSING_ID")
    if case.get("stage") not in ("RECOGNIZED", "SETTLED"):
        return blocked("NOT_RECOGNIZED")
    if case.get("owner_gate") != "APPROVED":
        return blocked("OWNER_GATE_CLOSED")
    if not str(case.get("evidence_uri") or "").strip():
        return blocked("MISSING_EVIDENCE")
    try:
        nums = {key: _money(case.get(key)) for key in MONEY_FIELDS}
    except ValueError:
        return blocked("MISSING_COST_OR_INVALID")
    mode = case.get("revenue_mode")
    if mode not in ("PRINCIPAL", "AGENT"):
        return blocked("MISSING_REVENUE_MODE")
    if mode == "AGENT":
        try:
            gmv = _money(case.get("gmv"))
        except ValueError:
            return blocked("AGENT_GMV_CHECK")
        if gmv < nums["reported_revenue"]:
            return blocked("AGENT_GMV_CHECK")
    cash = case.get("cash_collected")
    if cash is not None and cash != "":
        try:
            cash = _money(cash)
        except ValueError:
            return blocked("INVALID_CASH")
    else:
        cash = None  # UNKNOWN is not 0
    contribution = nums["reported_revenue"] - nums["direct_cost"] - nums["cac"] - nums["variable_support"]
    margin = (contribution / nums["reported_revenue"] if nums["reported_revenue"] else None)
    return {"case_id": case["case_id"], "status": "CALCULABLE_UNVERIFIED",
            "contribution": str(contribution),
            "contribution_margin": str(margin) if margin is not None else None,
            "cash_collected": str(cash) if cash is not None else None}


if __name__ == "__main__":
    payload = json.load(sys.stdin)
    if not isinstance(payload, list):
        raise SystemExit("Expected a JSON list of cases on stdin")
    json.dump([evaluate(item) for item in payload], sys.stdout, ensure_ascii=False, indent=2)
    print()
