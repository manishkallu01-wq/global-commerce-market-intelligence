"""Normalize extracted Schema.org Product nodes into the curated offer contract."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any


def _text(value: Any) -> str | None:
    if isinstance(value, dict):
        value = value.get("name")
    if value is None:
        return None
    result = str(value).strip()
    return result or None


def normalize_product(
    node: dict[str, Any], source_url: str, crawl_id: str, observed_at: str | None = None
) -> list[dict[str, Any]]:
    offers = node.get("offers") or []
    offers = offers if isinstance(offers, list) else [offers]
    rows: list[dict[str, Any]] = []
    for offer in offers or [{}]:
        if not isinstance(offer, dict):
            continue
        raw_price = offer.get("price") or offer.get("lowPrice")
        try:
            price = float(Decimal(str(raw_price))) if raw_price is not None else None
        except InvalidOperation:
            price = None
        currency = _text(offer.get("priceCurrency"))
        rows.append({
            "source_url": source_url,
            "crawl_id": crawl_id,
            "observed_at": observed_at or datetime.now(timezone.utc).isoformat(),
            "name": _text(node.get("name")),
            "brand": _text(node.get("brand")),
            "sku": _text(node.get("sku")),
            "gtin": _text(node.get("gtin13") or node.get("gtin")),
            "price": price,
            "currency": currency.upper() if currency else None,
            "availability": _text(offer.get("availability")),
            "seller": _text(offer.get("seller")),
        })
    return rows
