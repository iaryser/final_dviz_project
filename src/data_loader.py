import pandas as pd
import requests
import zipfile
import io
import os
from src.config import POPULATION_FILE_PATH, TERRORISM_FILE_PATH

def download_data(folder_path, file_name):
    url = 'https://www.kaggle.com/api/v1/datasets/download/START-UMD/gtd'

    if os.path.exists(file_name):
        return

    os.makedirs(folder_path, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(folder_path)


def prepare_terrorism_data(filepath):
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

    df = df[columns_to_keep]

    df['nkill'] = df['nkill'].fillna(0)
    df['nwound'] = df['nwound'].fillna(0)

    # Create casualties column
    df['casualties'] = df['nkill'] + df['nwound']

    return df


def get_map_data():
    pop_df = pd.read_csv(POPULATION_FILE_PATH)
    attacks_df = __TERRORISM_DF.groupby("country_txt").size().reset_index(name="attack_count")

    attacks_df = attacks_df.merge(pop_df, left_on="country_txt", right_on="country", how="left")

    attacks_df["attacks_per_million"] = attacks_df["attack_count"] / (attacks_df["population"] / 1_000_000)

    max_attacks = attacks_df["attacks_per_million"].max()

    bins = [0, 5, 15, 30, 60, 120, max_attacks]
    labels = ['0–5', '6–15', '16–30', '31–60', '61–120', f'121+']

    attacks_df["attack_bin"] = pd.cut(
        attacks_df["attacks_per_million"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return attacks_df, labels


def get_dropdown_options(field, filters: dict = {}):
    filtered_df = __TERRORISM_DF.copy()
    for key, val in filters.items():
        filtered_df = filtered_df[filtered_df[key] == val]

    available_types = filtered_df[field].dropna().unique()

    options = [{'label': t, 'value': t} for t in sorted(available_types)]

    return options


def get_donut_data(selected_attacks, filters: dict):
    filtered_df = __TERRORISM_DF.copy()
    for key, val in filters.items():
        filtered_df = filtered_df[filtered_df[key] == val]

    if selected_attacks:
        filtered_df = filtered_df[filtered_df['attacktype1_txt'].isin(selected_attacks)]

    filtered_df = filtered_df.groupby('attacktype1_txt').size().reset_index(name='count')
    filtered_df = filtered_df.sort_values(by='count', ascending=False).reset_index(drop=True)
    filtered_df['percentage'] = filtered_df['count']/filtered_df['count'].sum()

    threshold = 0.05

    large = filtered_df[filtered_df['percentage'] >= threshold]
    small = filtered_df[filtered_df['percentage'] < threshold]

    if small['count'].sum() > 0:
        other_row = pd.DataFrame([{
            'attacktype1_txt': 'Other',
            'count': small['count'].sum()
        }])

        filtered_df = pd.concat([large[['attacktype1_txt', 'count']], other_row], ignore_index=True)

    return filtered_df

def get_bar_data(filters: dict):
    filtered_df = __TERRORISM_DF.copy()
    for key, val in filters.items():
        filtered_df = filtered_df[filtered_df[key] == val]

    filtered_df = filtered_df.groupby('iyear').size().reset_index(name='count')

    return filtered_df


__TERRORISM_DF = prepare_terrorism_data(TERRORISM_FILE_PATH)
