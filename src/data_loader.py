import pandas as pd
import requests
import zipfile
import io
import os
from src.config import POPULATION_FILE_PATH


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

    df = df[columns_to_keep].copy()

    df['nkill'] = df['nkill'].fillna(0)
    df['nwound'] = df['nwound'].fillna(0)

    # Create casualties column
    df['casualties'] = df['nkill'] + df['nwound']

    return df

def calc_other_row_for_donut(data, threshold):
    large = data[data['percentage'] >= threshold]
    small = data[data['percentage'] < threshold]

    if small['count'].sum() > 0:
        other_row = pd.DataFrame([{
            'attacktype1_txt': 'Other',
            'count': small['count'].sum()
        }])

        return pd.concat([large[['attacktype1_txt', 'count']], other_row], ignore_index=True)
    else:
        return data


def filter_target_type_and_country(df, selected_target_type, clickData):
    filtered_df = df.copy()
    if selected_target_type:
        filtered_df = filtered_df[
            filtered_df['targtype1_txt'] == selected_target_type
        ]

    if clickData:
        country = clickData['points'][0]['location']
        filtered_df = filtered_df[filtered_df['country_txt'] == country]
    else:
        country = 'Global'

    return filtered_df, country


def get_map_data(df):
    pop_df = pd.read_csv(POPULATION_FILE_PATH)
    attacks_df = df.groupby("country_txt").size().reset_index(name="attack_count")

    attacks_df = attacks_df.merge(pop_df, left_on="country_txt", right_on="country", how="left")

    # Neue Spalte: Angriffe pro Million Einwohner
    attacks_df["attacks_per_million"] = attacks_df["attack_count"] / (attacks_df["population"] / 1_000_000)

    # Max-Wert holen (für letzte Binning-Stufe)
    max_attacks = attacks_df["attacks_per_million"].max()

    # Binning definieren (angepasst auf per-million Maßstab)
    bins = [0, 5, 15, 30, 60, 120, max_attacks]
    labels = ['0–5', '6–15', '16–30', '31–60', '61–120', f'121+']

    # Angriffe in Kategorien einteilen
    attacks_df["attack_bin"] = pd.cut(
        attacks_df["attacks_per_million"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return attacks_df, labels


def get_dropdown_options(filtered_df, field):
    available_types = filtered_df[field].dropna().unique()

    options = [{'label': t, 'value': t} for t in sorted(available_types)]

    return options
