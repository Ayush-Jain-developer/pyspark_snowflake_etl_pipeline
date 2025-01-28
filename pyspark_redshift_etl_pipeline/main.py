from transform import transform_data
from extract import authenticate_kaggle, download_dataset
from constant import NAME_BASICS_FILE_PATH, TITLE_RATINGS_FILE_PATH

def spark_etl_pipeline():
    api = authenticate_kaggle()
    download_dataset(api)
    transform_data(NAME_BASICS_FILE_PATH, TITLE_RATINGS_FILE_PATH)

if __name__ == "__main__":
    spark_etl_pipeline()

