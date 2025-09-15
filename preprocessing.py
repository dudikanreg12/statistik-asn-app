import pandas as pd
import numpy as np

def to_year(val):
    try:
        return pd.to_datetime(val, errors='coerce').year
    except:
        return np.nan

def classify_generation(y):
    if pd.isna(y): return np.nan
    y = int(y)
    if y <= 1964: return 'Baby Boomer'
    elif y <= 1980: return 'Gen X'
    elif y <= 1996: return 'Gen Y'
    elif y <= 2006: return 'Gen Z'
    return 'Lainnya'

def norm_status(x):
    s = str(x).lower()
    if 'aktif' in s: return 'Aktif'
    if 'pensiun' in s: return 'Pensiun'
    if 'bup' in s: return 'BUP'
    if 'cltn' in s: return 'CLTN'
    if 'hukuman' in s: return 'Hukuman Disiplin'
    if 'punah' in s: return 'Punah'
    return 'Lainnya'

def norm_pendidikan(x):
    s = str(x).lower()
    if 's3' in s: return 'S3'
    if 's2' in s: return 'S2'
    if 's1' in s or 'sarjana' in s: return 'S1'
    if 'd-4' in s: return 'D-IV'
    if 'd-3' in s: return 'D-III'
    if 'd-2' in s: return 'D-II'
    if 'd-1' in s: return 'D-I'
    if 'slta' in s and 'kejuruan' in s: return 'SLTA Kejuruan'
    if 'slta' in s and 'keguruan' in s: return 'SLTA Keguruan'
    if 'slta' in s: return 'SLTA'
    if 'sltp' in s: return 'SLTP'
    if 'sd' in s: return 'SD'
    return 'Lainnya'

def preprocess_data(df):
    df['tahun_lahir_year'] = df['tahun_lahir'].apply(to_year)
    df['generasi'] = df['tahun_lahir_year'].apply(classify_generation)
    df['status_kedudukan_norm'] = df['status_kedudukan'].apply(norm_status)
    df['pendidikan_detail'] = df['pendidikan'].apply(norm_pendidikan)

    df['jabatan'] = df['jabatan'].astype(str).str.lower()
    df['sub_jabatan'] = df.get('sub_jabatan', '').astype(str).str.lower()
    df['jabatan_struktural'] = np.where(df['jabatan'].str.contains('struktural', na=False), df['jabatan'], np.nan)
    df['jabatan_fungsional_tertentu'] = np.where(
        df['jabatan'].str.contains('fungsional', na=False) &
        df['sub_jabatan'].str.contains('guru|dosen|dokter|perawat|bidan|farmasi', na=False),
        df['jabatan'], np.nan
    )
    df['jabatan_fungsional_umum'] = np.where(
        df['jabatan'].str.contains('fungsional', na=False) &
        df['jabatan_fungsional_tertentu'].isna(),
        df['jabatan'], np.nan
    )
    return df
