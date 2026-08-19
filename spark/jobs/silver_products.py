"""Silver normalization and quarantine contract for parsed product offers."""
from pyspark.sql import SparkSession, functions as F
spark=SparkSession.builder.appName("commerce-silver").getOrCreate()
source=spark.table("commerce.bronze.product_offer_candidates")
clean = (
    source.withColumn("currency", F.upper(F.trim("currency")))
    .withColumn("price", F.col("price").cast("decimal(18,4)"))
    .withColumn(
        "quality_errors",
        F.array_compact(
            F.array(
                F.when(F.col("source_url").isNull(), F.lit("missing_source_url")),
                F.when(F.col("name").isNull(), F.lit("missing_name")),
                F.when(F.col("price").isNull() | (F.col("price") < 0), F.lit("invalid_price")),
                F.when(~F.col("currency").rlike("^[A-Z]{3}$"), F.lit("invalid_currency")),
            )
        ),
    )
)
clean.filter(F.size("quality_errors")==0).drop("quality_errors").write.mode("append").format("delta").option("mergeSchema","false").saveAsTable("commerce.silver.product_offers")
clean.filter(F.size("quality_errors")>0).write.mode("append").format("delta").saveAsTable("commerce.quarantine.product_offers")
