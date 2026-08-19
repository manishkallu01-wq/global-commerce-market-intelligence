#!/usr/bin/env python3
"""Discover genuine public-source records and write an immutable manifest."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from src.common_crawl import discover
from src.gdelt import latest_event_url

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--url", default="commoncrawl.org/get-started"); parser.add_argument("--crawl", default="CC-MAIN-2025-43"); parser.add_argument("--output", default="results/source_discovery/manifest.json"); args=parser.parse_args()
    result={"generated_at":datetime.now(timezone.utc).isoformat()}
    try:
        captures=discover(args.url,args.crawl,10); result["common_crawl"]={"status":"success","collection":args.crawl,"query":args.url,"captures":[c.to_dict() for c in captures]}
    except Exception as exc:
        result["common_crawl"]={"status":"failed","collection":args.crawl,"query":args.url,"error":f"{type(exc).__name__}: {exc}"}
    try: result["gdelt"]={"status":"success","latest_event_url":latest_event_url()}
    except Exception as exc: result["gdelt"]={"status":"failed","error":f"{type(exc).__name__}: {exc}"}
    path=Path(args.output); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
