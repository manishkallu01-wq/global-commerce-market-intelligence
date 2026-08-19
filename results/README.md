# Results

`sample_run/` contains committed outputs from the deterministic local fixture pipeline. These results prove extraction, normalization, metric generation and reproducibility; they do not represent a Common Crawl production run.

A real benchmark must publish the immutable input manifest, crawl ID, compressed source bytes, cluster configuration, job duration, row counts, reject reasons, throughput and cost. The repository does not substitute extrapolated numbers for measured results.

`source_discovery/live_manifest.json` is the recorded result of an actual Common Crawl CDX query. It resolved real WARC byte ranges. The GDELT request failed upstream during that run and is retained as a source-health signal.
