import unittest
from src.common_crawl import Capture, extract_http_payload
class CommonCrawlTest(unittest.TestCase):
    def test_capture_casts_ranges(self):
        c=Capture.from_cdx({"url":"https://x","timestamp":"1","filename":"f","offset":"10","length":"20","digest":"d","status":"200"}); self.assertEqual((c.offset,c.length),(10,20))
    def test_extracts_http_payload(self):
        warc=b'WARC/1.0\r\nX: y\r\n\r\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html>ok</html>'; self.assertEqual(extract_http_payload(warc),'<html>ok</html>')
