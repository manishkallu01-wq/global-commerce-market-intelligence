"""Databricks Bronze ingestion with source metadata and checkpoints."""
from pyspark.sql import SparkSession, functions as F, types as T
spark=SparkSession.builder.appName("commerce-bronze").getOrCreate()
schema=T.StructType([T.StructField("source_url",T.StringType()),T.StructField("crawl_id",T.StringType()),T.StructField("observed_at",T.TimestampType()),T.StructField("html",T.StringType()),T.StructField("source_digest",T.StringType())])
(spark.readStream.format("cloudFiles").option("cloudFiles.format","json").schema(schema).load(spark.conf.get("pipeline.raw_path"))
 .withColumn("ingested_at",F.current_timestamp()).withColumn("ingest_date",F.to_date("ingested_at"))
 .writeStream.format("delta").option("checkpointLocation",spark.conf.get("pipeline.bronze_checkpoint")).partitionBy("ingest_date").trigger(availableNow=True).toTable("commerce.bronze.web_pages"))
