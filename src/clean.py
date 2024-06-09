import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when, mean
from pyspark.sql.types import DoubleType, IntegerType, StringType

PATHS = None

def create_paths():
    global PATHS

    main_path = "cleaned_data"
    output_paths = {
        "min": os.path.join(main_path, "min"),
        "mean": os.path.join(main_path, "mean"),
        "max": os.path.join(main_path, "max")}

    for path in output_paths.values():
        os.makedirs(path, exist_ok=True)

    PATHS = output_paths

def create_spark_df():
    spark = SparkSession.builder \
        .appName("MyApp") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")


    min_df, mean_df, max_df = load_data(spark)
    df = [min_df, mean_df, max_df]

    min_df.printSchema()
    mean_df.printSchema()
    max_df.printSchema()

    clean_data(df)
    spark.stop()

def clean_data(dfs):
    cols = ["TN", "TG", "TX"]
    labels = ["min", "mean", "max"]


    for idx, df in enumerate(dfs):
        cleaned = df.withColumn(cols[idx], when(col(cols[idx]) == -9999, None).otherwise(col(cols[idx])))
        mean_val = cleaned.select(mean(col(cols[idx]))).collect()[0][0]

        cleaned = cleaned.fillna({cols[idx]: mean_val})
        corrected = correct_types(cleaned, idx, cols)

        save_data(corrected, labels, idx)
        # df.write.mode("overwrite").option("header", "true").csv(PATHS[labels[idx]])

    for path in PATHS.values():
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.crc'):
                    os.remove(os.path.join(root, file))


def correct_types(df,idx: int, cols: list):
    corrected = df.withColumn(cols[idx], (col(cols[idx])/ 10.0).cast(DoubleType())) \
        .withColumn("Q_"+cols[idx], col("Q_"+cols[idx]).cast(IntegerType())) \
        .withColumn("DATE", to_date(col("DATE").cast(StringType()), "yyyyMMdd")) \
        .withColumn("STAID", col("STAID").cast(IntegerType())) \
        .withColumn("SOUID", col("SOUID").cast(IntegerType()))

    corrected.printSchema()

    return corrected

def load_data(spark):
    main_path = "csv_data"
    input_paths = {
        "min": os.path.join(main_path, "min"),
        "mean": os.path.join(main_path, "mean"),
        "max": os.path.join(main_path, "max")
    }

    min_df = spark.read.csv(input_paths["min"], header=True, inferSchema=True)
    min_df = min_df.select([col(c).alias(c.strip()) for c in min_df.columns])

    mean_df = spark.read.csv(input_paths["mean"], header=True, inferSchema=True)
    mean_df = mean_df.select([col(c).alias(c.strip()) for c in mean_df.columns])


    max_df = spark.read.csv(input_paths["max"], header=True, inferSchema=True)
    max_df = max_df.select([col(c).alias(c.strip()) for c in max_df.columns])

    return min_df, mean_df, max_df


def save_data(df, labels, idx):
    df.write.mode("overwrite").option("header", "true").csv(PATHS[labels[idx]])



create_paths()
create_spark_df()
