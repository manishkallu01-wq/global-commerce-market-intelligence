"""Common Crawl CDX discovery and byte-range WARC retrieval."""
from __future__ import annotations
import gzip, json
from dataclasses import dataclass, asdict
from urllib.parse import urlencode
from urllib.request import Request, urlopen

INDEX_ROOT = "https://index.commoncrawl.org"
DATA_ROOT = "https://data.commoncrawl.org"

@dataclass(frozen=True)
class Capture:
    url: str; timestamp: str; filename: str; offset: int; length: int; digest: str; status: str
    @classmethod
    def from_cdx(cls, value: dict) -> "Capture":
        return cls(value["url"], value["timestamp"], value["filename"], int(value["offset"]), int(value["length"]), value["digest"], value["status"])
    def to_dict(self) -> dict: return asdict(self)

def discover(url_pattern: str, crawl: str = "CC-MAIN-2026-30", limit: int = 10) -> list[Capture]:
    query = urlencode({"url": url_pattern, "output": "json", "filter": "status:200", "limit": limit})
    request = Request(f"{INDEX_ROOT}/{crawl}-index?{query}", headers={"User-Agent": "commerce-intelligence/1.0"})
    with urlopen(request, timeout=60) as response:
        return [Capture.from_cdx(json.loads(line)) for line in response.read().decode().splitlines() if line]

def fetch_warc_record(capture: Capture) -> bytes:
    end = capture.offset + capture.length - 1
    request = Request(f"{DATA_ROOT}/{capture.filename}", headers={"Range": f"bytes={capture.offset}-{end}", "User-Agent": "commerce-intelligence/1.0"})
    with urlopen(request, timeout=120) as response: return gzip.decompress(response.read())

def extract_http_payload(warc: bytes) -> str:
    marker = b"\r\n\r\n"
    _, _, remainder = warc.partition(marker)
    _, _, payload = remainder.partition(marker)
    return payload.decode("utf-8", errors="replace")
