import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalisasi nama kolom
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Normalisasi jenis kelamin
    if "jenis_kelamin" in df.columns:
        df["jenis_kelamin"] = df["jenis_kelamin"].astype(str).str.upper().str.strip()
        df["jenis_kelamin"] = df["jenis_kelamin"].replace({
            "L": "Laki-laki", "LAKI-LAKI": "Laki-laki", "P": "Perempuan"
        })

    # Normalisasi status kedudukan
    if "status_kedudukan" in df.columns:
        df["status_kedudukan_norm"] = df["status_kedudukan"].astype(str).str.strip().str.title()

    # Normalisasi pendidikan
    if "pendidikan" in df.columns:
        df["pendidikan_norm"] = df["pendidikan"].astype(str).str.upper().str.strip()
        df["pendidikan_norm_detail"] = df["pendidikan_norm"].replace({
            "S-1": "S1", "S-2": "S2", "S-3": "S3", "D-IV": "D4", "D-III": "D3"
        })

    # Hitung usia jika ada kolom tahun lahir
    if "tahun_lahir" in df.columns:
        df["usia"] = 2025 - pd.to_numeric(df["tahun_lahir"], errors="coerce")

    return df
