import unittest

from lab.ledger import Ledger


class LedgerTests(unittest.TestCase):
    def test_same_reservation_retry_preserves_total(self):
        ledger = Ledger()
        self.assertEqual(ledger.settle("synthetic-reservation-a", 7), 7)
        self.assertEqual(ledger.settle("synthetic-reservation-a", 7), 7)
        self.assertEqual(ledger.settle("synthetic-reservation-a", 7), 7)
        self.assertEqual(ledger.total, 7)

    def test_distinct_reservations_accumulate(self):
        ledger = Ledger()
        self.assertEqual(ledger.settle("synthetic-reservation-a", 7), 7)
        self.assertEqual(ledger.settle("synthetic-reservation-b", 5), 12)
        self.assertEqual(ledger.settle("synthetic-reservation-c", 3), 15)
        self.assertEqual(ledger.total, 15)

    def test_conflicting_retry_preserves_original_settlement(self):
        ledger = Ledger()
        ledger.settle("synthetic-reservation-a", 7)
        with self.assertRaises(ValueError):
            ledger.settle("synthetic-reservation-a", 5)
        self.assertEqual(ledger.total, 7)
        self.assertEqual(ledger.settle("synthetic-reservation-a", 7), 7)

    def test_invalid_reservation_ids_do_not_change_state(self):
        for reservation_id in ("", None, 42, True, [], {}):
            with self.subTest(reservation_id=reservation_id):
                ledger = Ledger()
                ledger.settle("synthetic-reservation-a", 7)
                with self.assertRaises(ValueError):
                    ledger.settle(reservation_id, 5)
                self.assertEqual(ledger.total, 7)
                self.assertEqual(ledger.settle("synthetic-reservation-b", 5), 12)

    def test_invalid_amounts_do_not_change_or_reserve_state(self):
        for amount in (0, -1, True, False, 5.0, "5", None, [], {}):
            with self.subTest(amount=amount):
                ledger = Ledger()
                ledger.settle("synthetic-reservation-a", 7)
                with self.assertRaises(ValueError):
                    ledger.settle("synthetic-reservation-b", amount)
                self.assertEqual(ledger.total, 7)
                self.assertEqual(ledger.settle("synthetic-reservation-b", 5), 12)

    def test_existing_reservation_does_not_bypass_amount_validation(self):
        for amount in (True, 1.0):
            with self.subTest(amount=amount):
                ledger = Ledger()
                ledger.settle("synthetic-reservation-a", 1)
                with self.assertRaises(ValueError):
                    ledger.settle("synthetic-reservation-a", amount)
                self.assertEqual(ledger.total, 1)
