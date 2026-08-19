# Source strategy

## Common Crawl

Use the published crawl index and segment manifests to select WARC/WAT files. Store the source crawl ID, filename, byte range, fetch timestamp, HTTP metadata and content digest. Prefer WAT metadata during discovery; retrieve WARC payloads only where extraction requires page content.

Product observations come from Schema.org JSON-LD and supported microdata. The extractor must preserve the source URL and must not infer a price, inventory state, or identifier when the page does not provide one.

## GDELT

Poll published GDELT 2.1 update manifests, verify idempotency by filename and checksum, and publish normalized events to Kinesis. Entity and location matching must retain confidence and rule version.

## Data limitations

Crawl coverage is uneven across domains, languages and time. Markup quality varies. Listed prices may exclude tax, delivery, membership discounts or variants. These limitations are surfaced as coverage metrics and dashboard filters rather than hidden in transformations.
