"""GDELT 2.x last-update discovery and event ingestion."""
from __future__ import annotations
import csv, io, zipfile
from urllib.request import Request, urlopen

LATEST = "https://data.gdeltproject.org/gdeltv2/lastupdate.txt"

def latest_event_url() -> str:
    with urlopen(Request(LATEST, headers={"User-Agent": "commerce-intelligence/1.0"}), timeout=30) as response:
        lines = response.read().decode().splitlines()
    for line in lines:
        parts = line.split()
        if parts and parts[-1].endswith(".export.CSV.zip"): return parts[-1]
    raise ValueError("GDELT update manifest contains no event export")

def fetch_events(url: str, limit: int | None = None) -> list[list[str]]:
    with urlopen(Request(url, headers={"User-Agent": "commerce-intelligence/1.0"}), timeout=120) as response: payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        name = archive.namelist()[0]
        rows = csv.reader(io.TextIOWrapper(archive.open(name), encoding="utf-8"), delimiter="\t")
        result = []
        for row in rows:
            result.append(row)
            if limit and len(result) >= limit: break
        return result
