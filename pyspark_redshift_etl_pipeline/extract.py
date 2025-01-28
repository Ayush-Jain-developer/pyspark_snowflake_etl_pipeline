import os
import utils
import logging
from pathlib import Path
from constant import DATASET_NAME
from kaggle.api.kaggle_api_extended import KaggleApi

def authenticate_kaggle() -> KaggleApi:
    """creates kaggle api object for authentication

    Returns:
        KaggleApi: kaggle object
    """
    msg = 'Starting Kaggle Api authentication'
    try:
        logging.info(msg)
        api = KaggleApi()
        api.authenticate()
        return api
    except Exception as error_msg:
        logging.error(error_msg)

def download_dataset(kaggle_auth: KaggleApi, folder_name: Path='/app/movies-data', dataset_name: str=DATASET_NAME) -> None:
    """downloads given dataset from kaggle

    Args:
        kaggle_auth (KaggleApi): kaggle api object
        folder_name (Path, optional): Path to data folder. Defaults to 'movies_data'.
        dataset_name (str, optional): Name of the dataset to be extracted from kaggle.
    """

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        msg = f"Created folder {folder_name}"
        logging.info(msg)
        try:
            logging.info(f"Starting downloading kaggle dataset {dataset_name}")
            kaggle_auth.dataset_download_files(dataset_name, folder_name, unzip=True)
            logging.info(f'Downloaded dataset {dataset_name} in {folder_name}')
        except Exception as error_msg:
            logging.error(error_msg)
    else: 
        print("Data already mounted and present")



