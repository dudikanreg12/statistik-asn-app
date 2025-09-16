import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# KPI Ringkasan
# --------------------------
def _show_kpis(df: pd.DataFrame):
    total = len(df)
    usia_col = _first_available(df, ["usia", "umur"])
    usia_mean = df[usia_col].dropna().astype(float).mean() if usia_col else np.nan

    pend_col = _first_available(df, ["pendidikan_norm_detail", "pendidikan_norm", "pendidikan"])
    top_pend = (
        df[pend_col].dropna().astype(str).str.strip().value_counts().idxmax()
        if pend_col and df[pend_col].dropna().shape[0] > 0 else "-"
    )

    k1, k2, k3 = st.columns(3)
    k1.metric("Total ASN", f"{total:,}")
    k2.metric("Rata-rata Usia", f"{usia_mean:.1f}" if not np.isnan(usia_mean) else "—")
    k3.metric("Pendidikan Terbanyak", top_pend if top_pend else "—")


# --------------------------
# Charts
# --------------------------
def _plot_age_distribution(df: pd.DataFrame):
    col = _first_available(df, ["usia", "umur"])
    if not col:
        st.info("Kolom usia/umur tidak ditemukan.")
        return

    data = pd.to_numeric(df[col], errors="coerce").dropna()
    if data.empty:
        st.info("Tidak ada data usia yang valid.")
        return

    fig, ax = plt.subplots()
    ax.hist(data, bins=10, color="#4da3ff", edgecolor="white")
    ax.set_title("Distribusi Usia ASN")
    ax.set_xlabel("Usia")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig, clear_figure=True)


def _plot_gender_pie(df: pd.DataFrame):
    col = _first_available(df, ["jenis_kelamin", "jk", "gender"])
    if not col:
        st.info("Kolom jenis kelamin tidak ditemukan.")
        return

    s = (df[col]
         .dropna()
         .astype(str)
         .str.strip()
         .str.upper()
         .replace({"L": "Laki-laki", "LAKI-LAKI": "Laki-laki", "P": "Perempuan"}))
    counts = s.value_counts()
    if counts.empty:
        st.info("Tidak ada data jenis kelamin yang valid.")
        return

    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color=["#2f80ed", "#eb5757"])
    ax.set_title("Distribusi Jenis Kelamin ASN")
    ax.set_xlabel("Jumlah")
    st.pyplot(fig, clear_figure=True)


def simulate_cpns(df: pd.DataFrame, usia_threshold: int = 58):
    usia_col = _first_available(df, ["usia", "umur"])
    pend_col = _first_available(df, ["pendidikan_norm", "pendidikan"])

    if not usia_col or not pend_col:
        st.info("Kolom usia atau pendidikan tidak ditemukan.")
        return

    df_simulasi = df.copy()
    df_simulasi["siap_pensiun"] = df_simulasi[usia_col] >= usia_threshold
    pensiun_count = df_simulasi["siap_pensiun"].sum()

    st.markdown(f"### 🔄 Simulasi CPNS: ASN yang akan pensiun (usia ≥ {usia_threshold})")
    st.metric("Jumlah ASN Siap Pensiun", f"{pensiun_count:,}")

    vc = df_simulasi[df_simulasi["siap_pensiun"]][pend_col].dropna().value_counts().sort_values()
    if not vc.empty:
        fig, ax = plt.subplots(figsize=(6, max(3, len(vc) * 0.35)))
        ax.barh(vc.index, vc.values, color="#d63031")
        ax.set_title("Pendidikan ASN yang Siap Pensiun")
        ax.set_xlabel("Jumlah")
        st.pyplot(fig, clear_figure=True)


# --------------------------
# Helpers
# --------------------------
def _first_available(df: pd.DataFrame, candidates: list) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None
