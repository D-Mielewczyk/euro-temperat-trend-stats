import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min as spark_min, max as spark_max


def clear_output_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def move_single_csv(src_dir, dest_file):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".csv"):
                shutil.move(os.path.join(root, file), dest_file)
    shutil.rmtree(src_dir)


def main():
    output_dir = "output/top5_temperature_changes_detailed"
    summary_output_path = "output/top5_temperature_changes_summary.csv"
    temp_dir = "temp_output"

    clear_output_directory(output_dir)
    if os.path.exists(summary_output_path):
        os.remove(summary_output_path)
    clear_output_directory(temp_dir)

    spark = SparkSession.builder \
        .appName("DetectTop5TemperatureChanges") \
        .config("spark.sql.shuffle.partitions", "10") \
        .getOrCreate()

    cleaned_data_path = "src/cleaned_data"
    min_df = spark.read.csv(os.path.join(cleaned_data_path, "min"), header=True, inferSchema=True).repartition(10)
    max_df = spark.read.csv(os.path.join(cleaned_data_path, "max"), header=True, inferSchema=True).repartition(10)

    min_df = min_df.filter(col("Q_TN") == 0)
    max_df = max_df.filter(col("Q_TX") == 0)

    min_temp_changes = min_df.groupBy("STAID").agg(
        spark_min("TN").alias("min_temp"),
        spark_min("DATE").alias("min_temp_date")
    )

    max_temp_changes = max_df.groupBy("STAID").agg(
        spark_max("TX").alias("max_temp"),
        spark_max("DATE").alias("max_temp_date")
    )

    temp_changes_df = min_temp_changes.join(max_temp_changes, on="STAID", how="inner")

    temp_changes_df = temp_changes_df.withColumn(
        "temp_change",
        col("max_temp") - col("min_temp")
    ).orderBy(col("temp_change").desc()).cache()

    top5_areas_df = temp_changes_df.limit(5)

    top5_areas_df = top5_areas_df.withColumnRenamed("STAID", "Station ID") \
        .withColumnRenamed("min_temp", "Minimum Temperature") \
        .withColumnRenamed("max_temp", "Maximum Temperature") \
        .withColumnRenamed("min_temp_date", "Date of Minimum Temperature") \
        .withColumnRenamed("max_temp_date", "Date of Maximum Temperature") \
        .withColumnRenamed("temp_change", "Temperature Change")

    top5_staids = [row['Station ID'] for row in top5_areas_df.collect()]

    top5_min_df = min_df.filter(col("STAID").isin(top5_staids))
    top5_max_df = max_df.filter(col("STAID").isin(top5_staids))

    for staid in top5_staids:
        station_min_df = top5_min_df.filter(col("STAID") == staid)
        station_max_df = top5_max_df.filter(col("STAID") == staid)

        station_output_path_min = os.path.join(output_dir, f"station_{staid}_temperature_changes_min.csv")
        station_output_path_max = os.path.join(output_dir, f"station_{staid}_temperature_changes_max.csv")

        temp_output_path_min = os.path.join(temp_dir, f"temp_min_{staid}")
        temp_output_path_max = os.path.join(temp_dir, f"temp_max_{staid}")

        if station_min_df.head(1):
            station_min_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(temp_output_path_min)
            move_single_csv(temp_output_path_min, station_output_path_min)
        if station_max_df.head(1):
            station_max_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(temp_output_path_max)
            move_single_csv(temp_output_path_max, station_output_path_max)

    if top5_areas_df.head(1):
        top5_areas_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(temp_dir)
        move_single_csv(temp_dir, summary_output_path)

    spark.stop()


if __name__ == "__main__":
    main()
