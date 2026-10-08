import unittest

from lab.access import authorize
from lab.ledger import Ledger


class BaselineTests(unittest.TestCase):
    def test_matching_tenant(self):
        self.assertTrue(authorize({"tenant": "synthetic-a", "revoked": False}, "synthetic-a"))

    def test_different_tenant(self):
        self.assertFalse(authorize({"tenant": "synthetic-a", "revoked": False}, "synthetic-b"))

    def test_single_settlement(self):
        self.assertEqual(Ledger().settle("synthetic-reservation-1", 7), 7)
