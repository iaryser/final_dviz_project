import pandas as pd 

def prepare_data(filepath="data/global_terrorism_dataset.csv"):
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