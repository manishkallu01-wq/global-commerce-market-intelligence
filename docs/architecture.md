# Architecture decisions

## Storage and compute

S3 is the durable system of record. Raw crawl payloads are referenced by immutable manifests. Delta tables hold extracted and standardized observations. Databricks jobs scale independently from storage and checkpoint incremental progress. Glue provides shared catalog metadata.

Redshift receives conformed dimensions, facts, aggregates and materialized views. Loading raw WARC data into the warehouse would increase cost and weaken workload isolation. dbt owns warehouse transformations, tests, exposures and business definitions.

## Streaming

GDELT batches are detected every 15 minutes, normalized and placed on Kinesis so enrichment and risk alerts use the same replayable event contract. Kinesis is not used to pretend monthly crawl files are live events.

## Orchestration

EventBridge starts scheduled source discovery. Step Functions coordinates manifests, Databricks jobs, Glue checks, Redshift loads and dbt runs. Failed partitions can be replayed without restarting successful partitions.

## Scale controls

Partition work by crawl, segment and content hash. Compact small Delta files, cap concurrent downloads, apply back-pressure, and publish input-byte and cost metrics. Lifecycle policies move retained raw data to colder S3 tiers according to recovery requirements.
