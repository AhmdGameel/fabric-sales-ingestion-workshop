# Microsoft Fabric Sales Ingestion Workshop

This repository contains the resources used during my **Global Fabric Day** workshop.

## Architecture

```
CSV Files
    │
    ▼
OneLake (Landing)
    │
    ▼
Bronze (Raw)
    │
    ▼
Silver (Transformed)
    │
    ▼
Gold (Business Ready)
```

## Dataset

Upload the sample CSV files from the **data** folder into:

```
Files/landing
```

---

# Bronze Layer

Reads all CSV files from the Landing folder and performs an upsert into the Bronze Delta table using `order_id`.

```python
from delta.tables import DeltaTable

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("Files/landing/*.csv")
)

bronze_table = "bronze_sales"

if not spark.catalog.tableExists(bronze_table):

    df.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable(bronze_table)

else:

    bronze = DeltaTable.forName(spark, bronze_table)

    (
        bronze.alias("target")
        .merge(
            df.alias("source"),
            "target.order_id = source.order_id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
```

---

# Silver Layer

Reads the Bronze table and enriches the data by adding calculated business columns.

```python
from pyspark.sql.functions import *

bronze_df = spark.table("bronze_sales")

silver_df = (
    bronze_df
    .withColumn(
        "profit_margin_pct",
        round(
            (col("gross_profit_usd") / col("net_revenue_usd")) * 100,
            2
        )
    )
    .withColumn("order_year", year("order_date"))
    .withColumn("order_month", month("order_date"))
)

silver_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver_sales")
```

---

# Gold Layer

Creates a business-ready table by aggregating sales metrics per country.

```python
from pyspark.sql.functions import *

gold_df = (
    spark.table("silver_sales")
    .groupBy("country")
    .agg(
        sum("net_revenue_usd").alias("total_sales"),
        sum("gross_profit_usd").alias("total_profit"),
        count("*").alias("orders")
    )
)

gold_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold_sales")
```

---

## Project Flow

```
Landing CSV Files
        │
        ▼
bronze_sales
        │
        ▼
silver_sales
        │
        ▼
gold_sales
```

---
