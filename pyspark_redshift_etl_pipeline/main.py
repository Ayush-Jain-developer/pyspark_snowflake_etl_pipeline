from transform import transform_data
from extract import authenticate_kaggle, download_dataset
from constant import TITLE_RATINGS_FILE_PATH
from load_tables import load_tables

def spark_etl_pipeline():
    api = authenticate_kaggle()
    download_dataset(api)
    load_tables()
    transform_data(TITLE_RATINGS_FILE_PATH)
if __name__ == "__main__":
    spark_etl_pipeline()

