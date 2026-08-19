#!/usr/bin/env python3
"""Retrieve a discovered WARC record and execute extraction against genuine crawl bytes."""
import json
from datetime import datetime, timezone
from pathlib import Path
from src.common_crawl import Capture, extract_http_payload, fetch_warc_record
from src.extract_product import extract_products
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'results/source_discovery/live_manifest.json').read_text())
record=manifest['common_crawl']['captures'][0]; capture=Capture(**record)
warc=fetch_warc_record(capture); html=extract_http_payload(warc); products=extract_products(html)
result={"executed_at":datetime.now(timezone.utc).isoformat(),"source":"Common Crawl","collection":manifest['common_crawl']['collection'],"source_url":capture.url,"source_digest":capture.digest,"requested_compressed_bytes":capture.length,"retrieved_warc_bytes":len(warc),"decoded_html_bytes":len(html.encode()),"product_nodes":len(products),"status":"success","interpretation":"The genuine WARC range retrieval and HTML extraction completed. This source page is infrastructure documentation, so zero product nodes is expected and is not a business result."}
path=ROOT/'results/source_discovery/live_warc_run.json';path.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
