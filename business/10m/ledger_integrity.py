"""Offline, conservative audit of anonymized Xiaoyun 10M ledger rows.

A status ending in PROVISIONAL is NOT external proof, accounting approval,
or a statement of collected funds. Never writes to Google Sheets or a DB.
"""
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import sys


def _money(value):
    if value is None or value == "" or isinstance(value, bool):
        return None
    try:
        x = Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        return None
    return x if x.is_finite() and x >= 0 else None


def _date(value):
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        d = date.fromisoformat(value)
    except ValueError:
        return None
    return d if d.isoformat() == value else None


def audit(rows):
    """Require unique IDs, authorized review metadata and period dates.

    This only checks *shape/consistency*; the referenced evidence remains
    unverified. Unknown values are None, never quietly converted to zero.
    """
    if not isinstance(rows, list):
        raise ValueError("expected a JSON list")
    ids = Counter(str(r.get("case_id", "")).strip().casefold() for r in rows if isinstance(r, dict))
    out = []
    for row in rows:
        if not isinstance(row, dict):
            out.append({"case_id": None, "revenue_gate": "INVALID_ROW", "cash_gate": "REVENUE_GATE_BLOCKED", "provisional_revenue": None, "provisional_cash": None, "accounting_verified": False})
            continue
        key = str(row.get("case_id") or "").strip()
        gate = None
        if not key:
            gate = "MISSING_ID"
        elif ids[key.casefold()] != 1:
            gate = "DUPLICATE_ID"
        elif row.get("stage") not in ("RECOGNIZED", "SETTLED"):
            gate = "NOT_RECOGNIZED"
        elif row.get("owner_gate") != "APPROVED":
            gate = "OWNER_GATE_CLOSED"
        elif not str(row.get("source_uri") or "").strip() or not str(row.get("evidence_uri") or "").strip():
            gate = "MISSING_SOURCE"
        elif row.get("revenue_mode") not in ("PRINCIPAL", "AGENT"):
            gate = "MISSING_REVENUE_MODE"
        elif row.get("review_state") != "REVIEWED":
            gate = "REVIEW_PENDING"
        elif not str(row.get("review_reference") or "").strip():
            gate = "MISSING_REVIEW_REFERENCE"
        elif _date(row.get("recognition_date")) is None:
            gate = "RECOGNITION_DATE_MISSING"
        elif _money(row.get("reported_revenue")) is None:
            gate = "INVALID_REVENUE"
        elif _money(row.get("direct_cost")) is None:
            gate = "DIRECT_COST_UNKNOWN"
        elif row.get("revenue_mode") == "AGENT" and (
            _money(row.get("contract_estimate")) is None or
            _money(row.get("contract_estimate")) < _money(row.get("reported_revenue"))
        ):
            gate = "AGENT_GMV_RISK"
        else:
            gate = "REPORTING_PROVISIONAL"
        cash_gate = "REVENUE_GATE_BLOCKED"
        if gate == "REPORTING_PROVISIONAL":
            if row.get("stage") != "SETTLED":
                cash_gate = "NOT_SETTLED"
            elif _date(row.get("settlement_date")) is None:
                cash_gate = "SETTLEMENT_DATE_MISSING"
            elif _money(row.get("cash_collected")) is None:
                cash_gate = "CASH_UNKNOWN_OR_INVALID"
            else:
                cash_gate = "CASH_REPORTING_PROVISIONAL"
        out.append({
            "case_id": key or None,
            "revenue_gate": gate,
            "cash_gate": cash_gate,
            "provisional_revenue": str(_money(row.get("reported_revenue"))) if gate == "REPORTING_PROVISIONAL" else None,
            "provisional_cash": str(_money(row.get("cash_collected"))) if cash_gate == "CASH_REPORTING_PROVISIONAL" else None,
            "accounting_verified": False,
        })
    return out


if __name__ == "__main__":
    data = json.load(sys.stdin)
    json.dump(audit(data), sys.stdout, ensure_ascii=False, indent=2)
    print()
