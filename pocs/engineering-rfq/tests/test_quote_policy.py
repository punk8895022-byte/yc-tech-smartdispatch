import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quote_policy import build_vendor_line_rfq, check_poe_budget, calculate_internal_quote, release_gate


class RfqPolicyTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {'model': 'USG FLEX 100H', 'quantity': 1},
            {'model': 'GS1915-8EP', 'quantity': 1},
            {'model': 'NWA50AX', 'quantity': 4},
        ]

    def test_line_draft_has_correct_model_counts(self):
        draft = build_vendor_line_rfq(self.items)
        for expected in ('USG FLEX 100H × 1 台', 'GS1915-8EP × 1 台', 'NWA50AX × 4 台'):
            self.assertIn(expected, draft)
        self.assertIn('尚未確認採購', draft)

    def test_empty_items_fail(self):
        with self.assertRaises(ValueError):
            build_vendor_line_rfq([])

    def test_newline_in_model_fails(self):
        with self.assertRaises(ValueError):
            build_vendor_line_rfq([{'model': 'ok\nINJECT', 'quantity': 1}])

    def test_boolean_quantity_fails(self):
        with self.assertRaises(ValueError):
            build_vendor_line_rfq([{'model': 'AP', 'quantity': True}])

    def test_60w_is_insufficient_for_four_16w_aps(self):
        self.assertEqual('BLOCK', check_poe_budget(4, 16, 60)['status'])
        self.assertEqual('-4', check_poe_budget(4, 16, 60)['headroom_w'])

    def test_80w_passes_nominal_budget(self):
        self.assertEqual('PASS', check_poe_budget(4, 16, 80)['status'])

    def test_missing_price_rejected(self):
        with self.assertRaises(ValueError):
            calculate_internal_quote([{'quantity': 1, 'sell_ex_tax': 4000}])

    def test_synthetic_finance_math(self):
        q = calculate_internal_quote([
            {'quantity': 1, 'cost_ex_tax': 20000, 'sell_ex_tax': 24000},
            {'quantity': 1, 'cost_ex_tax': 4500, 'sell_ex_tax': 6000},
            {'quantity': 4, 'cost_ex_tax': 2500, 'sell_ex_tax': 3500},
        ])
        self.assertEqual('34500', q['cost_ex_tax'])
        self.assertEqual('44000', q['sell_ex_tax'])
        self.assertEqual('9500', q['gross_profit_ex_tax'])
        self.assertEqual('21.59', q['gross_margin_pct'])
        self.assertEqual('2200', q['vat'])
        self.assertEqual('46200', q['customer_total_inc_tax'])

    def test_owner_not_approved_blocks(self):
        self.assertEqual('HOLD', release_gate(vendor_prices_verified=True, poe_budget_pass=True, licensing_verified=True, owner_approved=False))

    def test_other_unverified_inputs_block(self):
        self.assertEqual('HOLD', release_gate(vendor_prices_verified=False, poe_budget_pass=True, licensing_verified=True, owner_approved=True))

    def test_all_verified_is_only_ready_to_manually_send(self):
        self.assertEqual('CUSTOMER_QUOTE_READY_FOR_MANUAL_SEND', release_gate(vendor_prices_verified=True, poe_budget_pass=True, licensing_verified=True, owner_approved=True))

    def test_nonboolean_gate_fails(self):
        with self.assertRaises(ValueError):
            release_gate(vendor_prices_verified='yes', poe_budget_pass=True, licensing_verified=True, owner_approved=True)

    def test_negative_money_rejected(self):
        with self.assertRaises(ValueError):
            calculate_internal_quote([{'quantity': 1, 'cost_ex_tax': -1, 'sell_ex_tax': 100}])


if __name__ == '__main__':
    unittest.main()
