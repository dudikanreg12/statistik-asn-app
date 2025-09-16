import streamlit as st
from data_loader import load_excel
from preprocessing import preprocess_data
from visuals import (
    _show_kpis,
    _plot_age_distribution,
    _plot_gender_pie,
    _plot_education_distribution,
    _plot_status_distribution,
    _plot_jabatan_distribution,
    plot_asn_per_kabupaten,
    simulate_cpns
)
from utils import show_sidebar_filters

st.set_page_config(page_title="Statistik ASN Aceh", layout="wide")

# 🏠 Halaman Pembuka
with st.container():
    st.markdown("<h1 style='text-align: center;'>📊 Statistik ASN Wilayah Kerja Aceh</h1>", unsafe_allow_html=True)
    # st.image("logo_aceh.png", width=100)  # Aktifkan jika ada logo
    st.markdown("""
    <div style='text-align: justify; font-size: 16px;'>
    Dashboard ini menyajikan data ASN secara visual dan interaktif untuk mendukung perencanaan SDM pemerintah daerah. 
    Fitur meliputi filter instansi, analisis demografi, simulasi CPNS, dan pencarian ASN.
    </div>
    """, unsafe_allow_html=True)

# 📁 Upload File
uploaded_file = st.file_uploader("📁 Upload file Excel ASN (.xlsx)", type=["xlsx"], key="file_asn")

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

        if df_filtered.empty:
            st.warning("Data kosong setelah filter. Coba ubah filter di sidebar.")
        else:
            # 🧭 Tab Navigasi
            tab_search, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "🔎 Cari ASN",
                "📊 Ringkasan & KPI",
                "👥 Usia & Jenis Kelamin",
                "🎓 Pendidikan & Status",
                "💼 Kategori Jabatan",
                "🌍 Sebaran Kabupaten",
                "🧪 Simulasi CPNS"
            ])

            with tab_search:
                search_term = st.text_input("Masukkan Nama atau NIP ASN")
                if search_term:
                    df_search = df_filtered[
                        df_filtered['nama'].astype(str).str.contains(search_term, case=False, na=False) |
                        df_filtered['nip'].astype(str).str.contains(search_term, case=False, na=False)
                    ]
                    if df_search.empty:
                        st.warning("ASN dengan kata kunci tersebut tidak ditemukan.")
                    else:
                        st.success(f"Ditemukan {len(df_search)} ASN yang cocok.")
                        st.dataframe(df_search)

            with tab1:
                _show_kpis(df_filtered)

            with tab2:
                c1, c2 = st.columns(2)
                with c1:
                    _plot_age_distribution(df_filtered)
                with c2:
                    _plot_gender_pie(df_filtered)

            with tab3:
                c3, c4 = st.columns(2)
                with c3:
                    _plot_education_distribution(df_filtered, use_detail_pendidikan)
                with c4:
                    _plot_status_distribution(df_filtered)

            with tab4:
                _plot_jabatan_distribution(df_filtered)

            with tab5:
                plot_asn_per_kabupaten(df_filtered)

            with tab6:
                simulate_cpns(df_filtered)

    except Exception as e:
        st.error(f"Terjadi error saat memproses data: {e}")
else:
    st.info("Silakan upload file Excel ASN untuk memulai.")
