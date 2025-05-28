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


def get_country_counts(df):
    # Angriffe pro Land zählen
    country_counts = df.groupby(
        "country_txt").size().reset_index(name="attack_count")

    max_attacks = country_counts['attack_count'].max()
    bins = [0, 250, 1215, 2743, 5235, 8306, max_attacks]

    labels = ['0-250', '251-1215', '1216-2743',
              '2744-5235', '5236-8306', '8307+']

    country_counts['attack_bin'] = pd.cut(
        country_counts['attack_count'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return country_counts, labels
