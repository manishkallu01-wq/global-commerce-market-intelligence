import unittest

from src.extract_product import extract_products


class ProductExtractionTest(unittest.TestCase):
    def test_extracts_product_from_graph(self):
        html = '''<script type="application/ld+json">{
          "@graph": [{"@type":"Product","name":"Trail Shoe","sku":"TS-1",
          "offers":{"@type":"Offer","price":"89.99","priceCurrency":"USD"}}]
        }</script>'''
        products = extract_products(html)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Trail Shoe")


    def test_ignores_malformed_json_ld(self):
        self.assertEqual(extract_products('<script type="application/ld+json">{bad}</script>'), [])


if __name__ == "__main__":
    unittest.main()
