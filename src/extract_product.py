"""Extract Schema.org Product JSON-LD from a public HTML page."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from typing import Any, Iterable


class _JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_json_ld = False
        self.buffer: list[str] = []
        self.payloads: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag.lower() == "script" and attributes.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.buffer = []

    def handle_data(self, data: str) -> None:
        if self.in_json_ld:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self.in_json_ld:
            self.payloads.append("".join(self.buffer))
            self.in_json_ld = False


def _nodes(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, list):
        for item in value:
            yield from _nodes(item)
    elif isinstance(value, dict):
        graph = value.get("@graph")
        if graph is not None:
            yield from _nodes(graph)
        yield value


def _is_product(node: dict[str, Any]) -> bool:
    node_type = node.get("@type", "")
    types = node_type if isinstance(node_type, list) else [node_type]
    return any(str(item).lower() == "product" for item in types)


def extract_products(html: str) -> list[dict[str, Any]]:
    """Return Product JSON-LD nodes; malformed scripts are quarantined by callers."""
    parser = _JsonLdParser()
    parser.feed(html)
    products: list[dict[str, Any]] = []
    for script in parser.payloads:
        try:
            payload = json.loads(script)
        except (json.JSONDecodeError, TypeError):
            continue
        products.extend(node for node in _nodes(payload) if _is_product(node))
    return products
