import unittest
from src.quality import split_quality
class QualityTest(unittest.TestCase):
    def test_quarantines_invalid_offer(self):
        good={"source_url":"https://example.test","crawl_id":"x","name":"shoe","price":10,"currency":"USD"}; bad={**good,"price":-1,"currency":"usd"}
        valid,rejected,counts=split_quality([good,bad]); self.assertEqual(len(valid),1); self.assertEqual(len(rejected),1); self.assertEqual(counts,{"invalid_currency":1,"negative_price":1})
