import pandas as pd
import requests
import zipfile
import io
import os

def download_data(folder_path, file_name):
    url = 'https://www.kaggle.com/api/v1/datasets/download/START-UMD/gtd'

    if os.path.exists(file_name):
        return

    os.makedirs(folder_path, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(folder_path)

def prepare_data(filepath):
    df = pd.read_csv(filepath, encoding="latin1")

    columns_to_keep = [
        'iyear',
        'country_txt',
        'attacktype1_txt',
        'nkill',
        'nwound',
        'gname',
        'targtype1_txt',
        'weaptype1_txt'
    ]

    df = df[columns_to_keep].copy()

    df['nkill'] = df['nkill'].fillna(0)
    df['nwound'] = df['nwound'].fillna(0)

    #Create casualties column
    df['casualties'] = df['nkill'] + df['nwound']

    return df
