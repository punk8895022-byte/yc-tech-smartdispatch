"""Xiaoyun engineering RFQ: offline policy only; no messaging, storage or production hooks."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

MONEY = Decimal('1')


def _amount(value):
    if isinstance(value, bool):
        raise ValueError('boolean is not a money amount')
    try:
        n = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError('invalid money amount') from None
    if not n.is_finite() or n < 0:
        raise ValueError('money amount must be finite and nonnegative')
    return n


def _qty(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError('quantity must be a positive integer')
    return value


def build_vendor_line_rfq(items):
    """Produce a draft to copy to LINE manually. Caller supplies generic item dictionaries."""
    if not items:
        raise ValueError('at least one item required')
    lines = ['您好，請協助提供以下設備之經銷報價，謝謝！', '', '【設備詢價｜草稿，尚未送出】']
    for i, item in enumerate(items, 1):
        model = str(item.get('model', '')).strip()
        if not model or any(c in model for c in '\r\n'):
            raise ValueError('model missing or contains newline')
        quantity = _qty(item.get('quantity'))
        lines.append(f'{i}. {model} × {quantity} 台')
    lines.extend([
        '',
        '請分列未稅單價、小計、5%營業稅與含稅總價，並註明現貨、交期、報價有效期限、保固與運費。',
        '防火牆請分列純硬體及包含資安訂閱授權的方案、授權內容與年限。',
        '請協助確認交換器 PoE 總預算能否支援四台 AP 的額定最大耗電；不足請提出替代型號與價格。',
        '此為詢價需求，尚未確認採購，謝謝。',
    ])
    return '\n'.join(lines)


def check_poe_budget(ap_quantity, rated_watts_each, switch_budget_watts):
    quantity = _qty(ap_quantity)
    rated = _amount(rated_watts_each)
    budget = _amount(switch_budget_watts)
    required = rated * quantity
    return {
        'required_w': str(required),
        'budget_w': str(budget),
        'headroom_w': str(budget - required),
        'status': 'PASS' if required <= budget else 'BLOCK',
    }


def calculate_internal_quote(lines, tax_rate='0.05'):
    """All unit prices EXCLUDE tax; output values are illustrative unless sourced."""
    if not lines:
        raise ValueError('at least one priced line required')
    rate = _amount(tax_rate)
    if rate > 1:
        raise ValueError('invalid tax rate')
    cost = Decimal('0')
    sell = Decimal('0')
    for item in lines:
        n = _qty(item.get('quantity'))
        if item.get('cost_ex_tax') is None or item.get('sell_ex_tax') is None:
            raise ValueError('unverified unit price missing')
        cost += _amount(item['cost_ex_tax']) * n
        sell += _amount(item['sell_ex_tax']) * n
    cost = cost.quantize(MONEY, rounding=ROUND_HALF_UP)
    sell = sell.quantize(MONEY, rounding=ROUND_HALF_UP)
    vat = (sell * rate).quantize(MONEY, rounding=ROUND_HALF_UP)
    profit = sell - cost
    margin = (profit / sell * 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if sell else None
    return {
        'cost_ex_tax': str(cost),
        'sell_ex_tax': str(sell),
        'gross_profit_ex_tax': str(profit),
        'gross_margin_pct': str(margin) if margin is not None else None,
        'vat': str(vat),
        'customer_total_inc_tax': str(sell + vat),
    }


def release_gate(*, vendor_prices_verified, poe_budget_pass, licensing_verified, owner_approved):
    """Fail closed; this does not send, publish or approve any quote."""
    flags = (vendor_prices_verified, poe_budget_pass, licensing_verified, owner_approved)
    if any(type(v) is not bool for v in flags):
        raise ValueError('all gate inputs must be explicit booleans')
    return 'CUSTOMER_QUOTE_READY_FOR_MANUAL_SEND' if all(flags) else 'HOLD'
