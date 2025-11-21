# Video Game Sales Dashboard - CEN445 Assignment
# Streamlit app for data visualization

import pandas as pd
import numpy as np
import streamlit as st

# =========================
# 1) DATA LOADING & PREPROCESSING
# =========================

@st.cache_data
def load_and_preprocess_data(csv_path: str, n_rows: int = 5000) -> pd.DataFrame:
    """
    Video game sales dataset'ini yükler, ilk n_rows satırı alır
    ve CEN445 ödev PDF'inde istenen preprocessing adımlarını uygular.
    """
    # 1) CSV'yi yükle
    df = pd.read_csv(csv_path)

    # 2) Sadece ilk 5000 satırı kullan
    df = df.head(n_rows).copy()

    # 3) Publisher'daki eksik değerleri 'Unknown' ile doldur
    if "Publisher" in df.columns:
        df["Publisher"] = df["Publisher"].fillna("Unknown")

    # 4) Year sütunundaki eksik değerleri at
    #    Çünkü yıl bilgisi zaman serisi ve trend analizleri için kritik
    if "Year" in df.columns:
        df = df.dropna(subset=["Year"])
        df["Year"] = df["Year"].astype(int)
        # On yıllık dönem (Decade)
        df["Decade"] = (df["Year"] // 10) * 10

    # 5) Satış kolonlarını numeric yap
    sales_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
    for col in sales_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # 6) Toplam bölgesel satış (NA+EU+JP+Other)
    if all(col in df.columns for col in ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]):
        df["Total_Regional_Sales"] = (
            df["NA_Sales"] +
            df["EU_Sales"] +
            df["JP_Sales"] +
            df["Other_Sales"]
        )

    # 7) Negatif satışları sıfıra çek (güvenlik amaçlı)
    for col in sales_cols + ["Total_Regional_Sales"]:
        if col in df.columns:
            df.loc[df[col] < 0, col] = 0.0

    # 8) Index reset
    df = df.reset_index(drop=True)

    return df


def filter_data(df: pd.DataFrame, genre: str, platforms: list, year_range: tuple, top_n: int | None):
    """
    Sidebar filtrelerine göre veriyi süzer.
    """
    filtered = df.copy()

    # Genre filtresi
    if genre != "All":
        filtered = filtered[filtered["Genre"] == genre]

    # Platform filtresi
    if platforms:
        filtered = filtered[filtered["Platform"].isin(platforms)]

    # Yıl aralığı filtresi
    if "Year" in filtered.columns:
        filtered = filtered[
            (filtered["Year"] >= year_range[0]) &
            (filtered["Year"] <= year_range[1])
        ]

    # Global satışa göre sıralayıp top_n alma (opsiyonel)
    if top_n is not None and "Global_Sales" in filtered.columns:
        filtered = filtered.sort_values("Global_Sales", ascending=False).head(top_n)

    return filtered


if __name__ == "__main__":
    st.write("Data loading functions ready!")
