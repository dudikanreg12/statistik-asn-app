import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def show_visualizations(df, instansi, jabatan, status, use_detail_pendidikan):
    if df.empty:
        st.warning("Data kosong setelah filter. Silakan ubah filter.")
        return

    gen_order = ['Baby Boomer','Gen X','Gen Y','Gen Z','Lainnya']
    gen_count = df['generasi'].value_counts().reindex(gen_order).fillna(0)
    fig1, ax1 = plt.subplots()
    gen_count.plot(kind='bar', color=['#7C4DFF','#00B8D9','#36B37E','#FFAB00','#B3BAC5'], ax=ax1)
    ax1.set_ylabel("Jumlah ASN")
    ax1.set_xlabel("Generasi")
    st.pyplot(fig1)

    pend_col = 'pendidikan_detail' if use_detail_pendidikan else 'pendidikan'
    pend_count = df[pend_col].value_counts().fillna(0)
    fig2, ax2 = plt.subplots()
    pend_count.plot(kind='bar', color='#0B84A5', ax=ax2)
    ax2.set_ylabel("Jumlah ASN")
    ax2.set_xlabel("Pendidikan")
    st.pyplot(fig2)

    jab_series = pd.Series({
        'Struktural': df['jabatan_struktural'].notna().sum(),
        'Fungsional Tertentu': df['jabatan_fungsional_tertentu'].notna().sum(),
        'Fungsional Umum': df['jabatan_fungsional_umum'].notna().sum()
    }).fillna(0).astype(int)
    jab_series = jab_series[jab_series > 0]
    if not jab_series.empty:
        fig3, ax3 = plt.subplots()
        jab_series.plot.pie(autopct='%1.0f%%', colors=['#4C78A8','#F58518','#54A24B'], ax=ax3)
        ax3.set_ylabel("")
        st.pyplot(fig3)

    st.subheader("📋 Ringkasan KPI")
    kpi = {
        'Jumlah ASN': len(df),
        'Proporsi Baby Boomer (%)': round((df['generasi']=='Baby Boomer').mean()*100,1),
        'Proporsi Gen Z (%)': round((df['generasi']=='Gen Z').mean()*100,1),
        'Proporsi S1+ (%)': round(df['pendidikan'].isin(['S1','S2','S3']).mean()*100,1),
        'Proporsi Struktural (%)': round(df['jabatan_struktural'].notna().mean()*100,1),
        'Proporsi Aktif (%)': round((df['status_kedudukan_norm']=='Aktif').mean()*100,1)
    }
    st.dataframe(pd.DataFrame(kpi.items(), columns=['Indikator','Nilai']))

    st.subheader("📥 Unduh Data Hasil Filter")
    filename = f"asn_{instansi}_{jabatan}_{status}.csv".replace(' ', '_')
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name=filename, mime='text/csv')
