# Sample run interpretation

The run processed two deterministic HTML fixtures containing three valid product offers. All offers passed the minimum name, currency and price checks, producing a 100% valid-offer rate. Two observations describe the same GTIN from different sellers, demonstrating the input needed for price-position analysis. Their prices differ by $10.00; this is a fixture-level check, not evidence about a real market.

The output also retains availability. One seller lists the shared product as in stock and another as out of stock, which exercises the availability-risk model. Production dashboards must show seller count and crawl coverage beside these metrics so users do not mistake sparse web observations for complete market inventory.

No rows were quarantined in this fixture run. `quarantine.json` is still emitted on every run so malformed or incomplete observations remain auditable rather than disappearing from totals.
