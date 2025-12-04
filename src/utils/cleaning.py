import pandas as pd
import numpy as np
import re

def clean_tracks_raw(df: pd.DataFrame):
    df = df.dropna().copy()

    df['trackTitle'] = df['trackTitle'].str.replace(r'[\(\[]\s*(feat|ft|with)[^\)\]]*[\)\]]', '', regex=True, flags=re.IGNORECASE).str.strip()
    df['trackTitle'] = df['trackTitle'].str.replace(r'(\s*[-–—]?\s+(?:feat|ft|featuring)\b.*$)', '', regex=True, flags=re.IGNORECASE).str.strip()

    df['artists_tuple'] = df['artists'].apply(lambda x: tuple(x) if isinstance(x, (list, np.ndarray)) else x)
    df = df.drop_duplicates(subset=['trackTitle', 'artists_tuple'], keep='first').reset_index(drop=True)
    df = df.drop(columns=['artists_tuple'])

    df.rename(columns={'durationMs': 'durationMin'}, inplace=True)
    df['durationMin'] = df['durationMin'] / 60000

    return df
