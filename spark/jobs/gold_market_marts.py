"""Gold market aggregates consumed by Redshift and dashboards."""
from pyspark.sql import SparkSession, functions as F
spark=SparkSession.builder.appName("commerce-gold").getOrCreate(); offers=spark.table("commerce.silver.product_offers")
key=F.coalesce("gtin","sku","name")
gold=(offers.groupBy(key.alias("product_key"),"currency",F.to_date("observed_at").alias("observation_date"))
 .agg(F.count("*").alias("offer_count"),F.countDistinct("seller").alias("seller_count"),F.min("price").alias("minimum_price"),F.expr("percentile_approx(price, 0.5)").alias("median_price"),F.max("price").alias("maximum_price"),F.avg(F.when(F.col("availability").endswith("InStock"),1).otherwise(0)).alias("availability_rate")))
gold.write.mode("overwrite").format("delta").option("overwriteSchema","true").saveAsTable("commerce.gold.market_daily")
