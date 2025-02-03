import os
from pyspark.sql import SparkSession
from constant import TITLE_BASICS_FILE_PATH

spark = SparkSession.builder.appName("spark_etl_pipeline").getOrCreate() 

csv_file_paths = {
    TITLE_BASICS_FILE_PATH: "title_ratings"
}

def transform_data(df):
    return df

def write_to_snowflake(df, table_name):
    df.write.format("net.snowflake.spark.snowflake") \
    .option("sfURL", os.getenv("SNOWFLAKE_ACCOUNT")) \
    .option("sfDatabase", os.getenv("SNOWFLAKE_DATABASE")) \
    .option("sfSchema", os.getenv("SNOWFLAKE_SCHEMA")) \
    .option("sfUser", os.getenv("SNOWFLAKE_USERNAME")) \
    .option("sfPassword", os.getenv("SNOWFLAKE_PASSWORD")) \
    .option("sfWarehouse", os.getenv("SNOWFLAKE_WAREHOUSE")) \
    .option("dbTable", table_name) \
    .mode("overwrite").save()

def process_csv_file(file_path, table_name):

    try:
        df = spark.read.csv(file_path, sep='\t', header=True, inferSchema=True)
        df = transform_data(df)
        write_to_snowflake(df, table_name)
    except Exception as e:
        print(f"Error occurred: {e}")

for file, table_name in csv_file_paths:
    process_csv_file(file, table_name)

