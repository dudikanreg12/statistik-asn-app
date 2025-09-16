import streamlit as st

def show_sidebar_filters(df):
    st.sidebar.header("🔎 Filter Data")

    instansi_list = sorted(df['instansi'].dropna().unique())
    selected_instansi = st.sidebar.selectbox("Instansi", instansi_list)

    jabatan_options = ['Semua', 'Struktural', 'Fungsional Tertentu', 'Fungsional Umum']
    selected_jabatan = st.sidebar.selectbox("Kategori Jabatan", jabatan_options)

    status_options = ['Semua', 'Aktif', 'Pensiun', 'BUP', 'CLTN', 'Hukuman Disiplin', 'Punah', 'Lainnya']
    selected_status = st.sidebar.selectbox("Status Kedudukan", status_options)

    use_detail_pendidikan = st.sidebar.checkbox("Gunakan kategori pendidikan detail", value=True)

    return selected_instansi, selected_jabatan, selected_status, use_detail_pendidikan
