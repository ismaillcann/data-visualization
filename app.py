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


# =========================
# 2) STREAMLIT APP LAYOUT
# =========================

def main():
    st.set_page_config(
        page_title="Video Game Sales Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🎮 Video Game Sales Exploratory Dashboard")
    st.markdown(
        """
        This dashboard was created for the CEN445 *Introduction to Data Visualization* assignment using the **video game sales** dataset.
        
        - Dataset: Kaggle - Video Game Sales  
        - Number of rows: First 5,000 records  
        - Purpose: To generate meaningful insights using different visualization techniques
        """
    )

    # -- Veriyi yükle ve preprocess et
    df = load_and_preprocess_data("vgsales.csv", n_rows=5000)

    # ===========
    # SIDEBAR FILTERS (En az 3 interaktif bileşen)
    # ===========
    st.sidebar.header("Filters")

    # Genre seçimi
    genres = ["All"] + sorted(df["Genre"].dropna().unique().tolist())
    selected_genre = st.sidebar.selectbox("Genre", genres)

    # Platform seçimi
    platforms = sorted(df["Platform"].dropna().unique().tolist())
    selected_platforms = st.sidebar.multiselect(
        "Platforms",
        platforms,
        default=[]
    )

    # Year aralığı
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())
    selected_year_range = st.sidebar.slider(
        "Year Range",
        min_year,
        max_year,
        (min_year, max_year),
        step=1
    )

    # Sadece top N oyunları gösterme seçeneği
    top_n_option = st.sidebar.selectbox(
        "Top N games by Global Sales (optional)",
        options=["All", 50, 100, 200]
    )
    top_n_value = None if top_n_option == "All" else int(top_n_option)

    # Filtrelenmiş veri
    filtered_df = filter_data(
        df,
        genre=selected_genre,
        platforms=selected_platforms,
        year_range=selected_year_range,
        top_n=top_n_value
    )

    st.sidebar.markdown(f"**Filtered rows:** {len(filtered_df)}")

    # ===========
    # MAIN TABS
    # ===========
    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview",
        "Sales by Time & Genre",
        "Top Games & Distributions",
        "Advanced Visualizations"
    ])

    # -------------------
    # TAB 1: OVERVIEW
    # -------------------
    with tab1:
        st.subheader("Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Games (filtered)", len(filtered_df))
        with col2:
            st.metric("Distinct Platforms", filtered_df["Platform"].nunique())
        with col3:
            st.metric("Distinct Genres", filtered_df["Genre"].nunique())
        with col4:
            st.metric("Total Global Sales (M)", round(filtered_df["Global_Sales"].sum(), 2))

        st.markdown("### Sample of Filtered Data")
        st.dataframe(filtered_df.head(20))


if __name__ == "__main__":
    main()
