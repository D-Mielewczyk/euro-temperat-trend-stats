import logging
import os
import pyspark.sql
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when, mean, year, lit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_spark_session():
    """ Spark setup and handling data """
    spark = SparkSession.builder \
        .appName("VisualizationPrep") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark

def load_data(spark, path):
    """ Loading csv data to dataframes and removing spaces """
    df = spark.read.csv(path, header=True, inferSchema=True)
    df = df.select([col(c).alias(c.strip()) for c in df.columns])
    return df

def save_yearly_avg(df, temp_col, quality_col, output_dir):
    # Add YEAR column
    df = df.withColumn("YEAR", year("DATE"))
    
    # Calculate yearly averages
    avg_df = df.groupBy("STAID", "SOUID", "YEAR").agg(
        mean(temp_col).alias(temp_col)
    ).withColumn(quality_col, lit(0))  # Adding quality column as zero
    logging.info(f"Finished calculating average data for {output_dir}")

    # Save data for each station separately

    os.makedirs(output_dir, exist_ok=True)


    df_repartitioned = avg_df.repartition("STAID")
    df_repartitioned.write.partitionBy("STAID").mode("overwrite").option("header", True).csv(output_dir)


    logging.info(f"Finished saving data to {output_dir}")



def get_line_plot_data(spark):
    # Process min temperatures
    logging.info(f"Loading data from cleaned_data/min")
    min_df = load_data(spark, "cleaned_data/min")
    logging.info(f"Processing min data")
    save_yearly_avg(min_df, "TN", "Q_TN", "line_plot_data/min")
    
    # Process mean temperatures
    logging.info(f"Loading data from cleaned_data/mean")
    mean_df = load_data(spark, "cleaned_data/mean")
    logging.info(f"Processing mean data")
    save_yearly_avg(mean_df, "TG", "Q_TG", "line_plot_data/mean")

    # Process max temperatures
    logging.info(f"Loading data from cleaned_data/max")
    max_df = load_data(spark, "cleaned_data/max")
    logging.info(f"Processing max data")
    save_yearly_avg(max_df, "TX", "Q_TX", "line_plot_data/max")

if __name__ == "__main__":
    # spark = create_spark_session()

    spark = SparkSession.builder \
    .master('local[*]') \
    .config("spark.driver.memory", "6g") \
    .appName('my-cool-app') \
    .getOrCreate()

    # Przygotowanie danych do line plot
    get_line_plot_data(spark)

    spark.stop()
