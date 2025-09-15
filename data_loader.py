import pandas as pd

def load_excel(file):
    df = pd.read_excel(file)
    df.columns = [str(c).strip().lower().replace('_',' ').replace('-',' ') for c in df.columns]
    col_map = {
        'instansi': ['instansi', 'unit kerja', 'opd', 'nama instansi'],
        'tahun_lahir': ['tahun lahir', 'thn lahir', 'tgl lahir'],
        'jenis_kelamin': ['jenis kelamin', 'jk', 'gender'],
        'pendidikan': ['pendidikan', 'pendidikan terakhir'],
        'golongan': ['golongan', 'golongan ruang'],
        'jabatan': ['jabatan', 'jenis jabatan'],
        'sub_jabatan': ['sub jabatan', 'kategori fungsional'],
        'status_kedudukan': ['status kedudukan', 'status']
    }
    renamed = {}
    for std_col, variants in col_map.items():
        for v in variants:
            for col in df.columns:
                if v in col and std_col not in renamed.values():
                    renamed[col] = std_col
                    break
    df.rename(columns=renamed, inplace=True)
    return df
