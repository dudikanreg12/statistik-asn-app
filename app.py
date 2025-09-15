import streamlit as st
from data_loader import load_excel
from preprocessing import preprocess_data
from visuals import show_visualizations
from utils import show_sidebar_filters

st.set_page_config(page_title="Statistik ASN Aceh", layout="wide")
st.title("📊 Statistik ASN Wilayah Kerja Aceh")

uploaded_file = st.file_uploader("📁 Upload file Excel ASN (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df_raw = load_excel(uploaded_file)
        df = preprocess_data(df_raw)

        selected_instansi, selected_jabatan, selected_status, use_detail_pendidikan = show_sidebar_filters(df)

        df_filtered = df[df['instansi'] == selected_instansi].copy()
        if selected_jabatan != 'Semua':
            key = f"jabatan_{selected_jabatan.lower().replace(' ', '_')}"
            if key in df_filtered.columns:
                df_filtered = df_filtered[df_filtered[key].notna()]
        if selected_status != 'Semua':
            df_filtered = df_filtered[df_filtered['status_kedudukan_norm'] == selected_status]

        show_visualizations(df_filtered, selected_instansi, selected_jabatan, selected_status, use_detail_pendidikan)
    except Exception as e:
        st.error(f"Terjadi error saat memproses data: {e}")
else:
    st.info("Silakan upload file Excel ASN untuk memulai.")
