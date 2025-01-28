import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark_etl_pipeline").getOrCreate()


def transform_data(file_path, title_file_path):
    df = None
    titles_df = None
    
    if os.path.exists(file_path):
        df = spark.read.csv(file_path, sep='\t', header=True, inferSchema=True)

    if os.path.exists(title_file_path):
        titles_df = spark.read.csv(title_file_path, sep='\t', header=True, inferSchema=True)

    else:
        print(f"{title_file_path} does not exist")
    
    chunked_df = df.repartition(3)
    chunked_df_titles = titles_df.repartition(3)

    def process_partition(iterator):
        count = 0
        for _ in iterator:
            count += 1

    def process_titles(iterator):
        count = 0
        for _ in iterator:
            count += 1

    chunked_df.foreachPartition(process_partition)
    chunked_df_titles.foreachPartition(process_titles)

