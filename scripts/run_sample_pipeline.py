#!/usr/bin/env python3
"""Run the deterministic fixture pipeline and publish auditable sample results."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from src.extract_product import extract_products
from src.normalize_offer import normalize_product


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source_dir = ROOT / "tests/fixtures/pages"
    output_dir = ROOT / "results/sample_run"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    attempted = 0
    source_bytes = 0
    for path in sorted(source_dir.glob("*.html")):
        html = path.read_text()
        source_bytes += path.stat().st_size
        attempted += 1
        for node in extract_products(html):
            rows.extend(normalize_product(
                node,
                f"https://fixture.invalid/{path.name}",
                "LOCAL-FIXTURE",
                "2026-01-01T00:00:00+00:00",
            ))
    fields = ["source_url", "crawl_id", "observed_at", "name", "brand", "sku", "gtin", "price", "currency", "availability", "seller"]
    with (output_dir / "product_offers.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    valid = [row for row in rows if row["name"] and row["currency"] and row["price"] is not None]
    summary = {
        "run_type": "deterministic_local_fixture",
        "source_pages": attempted,
        "source_bytes": source_bytes,
        "product_offer_rows": len(rows),
        "valid_offer_rows": len(valid),
        "valid_offer_rate": round(len(valid) / len(rows), 4) if rows else 0,
        "distinct_brands": len({row["brand"] for row in valid if row["brand"]}),
        "currencies": sorted({row["currency"] for row in valid}),
        "production_claim": False,
    }
    (output_dir / "metrics.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
