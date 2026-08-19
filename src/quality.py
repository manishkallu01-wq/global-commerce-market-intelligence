"""Curated offer validation with explicit reject reasons."""
from __future__ import annotations
from collections import Counter

def validate_offer(row: dict) -> list[str]:
    errors=[]
    if not row.get("source_url"): errors.append("missing_source_url")
    if not row.get("crawl_id"): errors.append("missing_crawl_id")
    if not row.get("name"): errors.append("missing_name")
    if row.get("price") is None: errors.append("missing_price")
    elif row["price"] < 0: errors.append("negative_price")
    currency=row.get("currency")
    if not currency or len(currency) != 3 or not currency.isupper(): errors.append("invalid_currency")
    return errors

def split_quality(rows: list[dict]) -> tuple[list[dict], list[dict], dict[str,int]]:
    valid, rejected, counts = [], [], Counter()
    for row in rows:
        errors=validate_offer(row)
        if errors:
            rejected.append({**row, "reject_reasons": errors}); counts.update(errors)
        else: valid.append(row)
    return valid, rejected, dict(sorted(counts.items()))
