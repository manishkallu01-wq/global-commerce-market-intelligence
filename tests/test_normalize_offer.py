import unittest

from src.normalize_offer import normalize_product


class NormalizeOfferTest(unittest.TestCase):
    def test_normalizes_nested_values(self):
        node = {"name": "Shoe", "brand": {"name": "Acme"}, "offers": {"price": "12.50", "priceCurrency": "usd"}}
        row = normalize_product(node, "https://example.invalid/p", "TEST")[0]
        self.assertEqual(row["brand"], "Acme")
        self.assertEqual(row["currency"], "USD")
        self.assertEqual(row["price"], 12.5)
