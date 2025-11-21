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

    # -------------------
    # TAB 2: TIME & GENRE ANALYSIS
    # -------------------
    with tab2:
        st.subheader("📈 Global Sales Over Time")

        import plotly.express as px

        # 1) Line Chart: Year vs Global Sales (basit ama anlamlı)
        yearly_sales = (
            filtered_df.groupby("Year", as_index=False)["Global_Sales"]
            .sum()
            .sort_values("Year")
        )

        fig_line = px.line(
            yearly_sales,
            x="Year",
            y="Global_Sales",
            markers=True,
            title="Global Sales by Year",
        )
        fig_line.update_layout(hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)

        # 2) Genre bazlı yıllık satış – stacked area veya bar
        st.subheader("🎭 Genre-wise Sales Over Time")

        genre_year = (
            filtered_df.groupby(["Year", "Genre"], as_index=False)["Global_Sales"]
            .sum()
        )

        fig_area = px.area(
            genre_year,
            x="Year",
            y="Global_Sales",
            color="Genre",
            title="Genre-wise Global Sales Over Time",
        )
        st.plotly_chart(fig_area, use_container_width=True)

    # -------------------
    # TAB 3: TOP GAMES & DISTRIBUTIONS
    # -------------------
    with tab3:
        st.subheader("🏆 Top Games by Global Sales")

        # 3) Bar Chart: En çok satan oyunlar
        top_games = (
            filtered_df.sort_values("Global_Sales", ascending=False)
            .head(20)
        )

        fig_bar = px.bar(
            top_games,
            x="Name",
            y="Global_Sales",
            color="Platform",
            title="Top 20 Games by Global Sales",
            hover_data=["Genre", "Publisher", "Year"],
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

        # 4) Genre ↔ Platform Sankey Flow
        st.subheader("📦 Genre ↔ Platform Sales Flow")

        import plotly.graph_objects as go

        sankey_df = (
            filtered_df.groupby(["Genre", "Platform"], as_index=False)["Global_Sales"]
            .sum()
            .sort_values("Global_Sales", ascending=False)
            .head(200)
        )
        genre_nodes = sankey_df["Genre"].unique().tolist()
        platform_nodes = sankey_df["Platform"].unique().tolist()
        all_nodes = genre_nodes + platform_nodes
        node_indices = {name: idx for idx, name in enumerate(all_nodes)}

        palette = px.colors.qualitative.Set3
        genre_colors = {
            genre: palette[i % len(palette)] for i, genre in enumerate(genre_nodes)
        }
        node_colors = [
            genre_colors.get(node, "#6c757d") for node in all_nodes
        ]
        default_link_color = "rgba(255, 255, 255, 0.25)"
        link_hover_colors = sankey_df["Genre"].map(genre_colors).tolist()

        sankey_fig = go.Figure(
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=15,
                    thickness=15,
                    label=all_nodes,
                    color=node_colors,
                ),
                link=dict(
                    source=sankey_df["Genre"].map(node_indices).tolist(),
                    target=sankey_df["Platform"].map(node_indices).tolist(),
                    value=sankey_df["Global_Sales"].tolist(),
                    color=[default_link_color] * len(sankey_df),
                    hovercolor=link_hover_colors,
                ),
            )
        )
        sankey_fig.update_layout(title="Genre → Platform Global Sales Flow")
        st.plotly_chart(sankey_fig, use_container_width=True)

    # -------------------
    # TAB 4: ADVANCED VISUALIZATIONS
    # -------------------
    with tab4:
        st.subheader("🚀 Advanced Visualizations")

        # 5) Treemap: Genre -> Publisher bazlı global satış
        st.markdown("#### Treemap: Genre / Publisher / Game Hierarchy")

        treemap_df = filtered_df.copy()
        # Çok fazla publisher ve oyun varsa, biraz filtreleyelim (önce en çok satanlardan)
        treemap_df = treemap_df.sort_values("Global_Sales", ascending=False).head(500)

        fig_treemap = px.treemap(
            treemap_df,
            path=["Genre", "Publisher", "Name"],
            values="Global_Sales",
            title="Treemap of Global Sales by Genre → Publisher → Game",
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

        # 6) Parallel Coordinates: Bölgesel satışların karşılaştırılması
        st.markdown("#### Parallel Coordinates: Regional vs Global Sales")

        # Sadece birkaç oyun alalım, yoksa grafik karışır
        pc_df = filtered_df.sort_values("Global_Sales", ascending=False).head(200)

        # Parallel coordinates için sadece satış kolonlarını kullanıyoruz
        pc_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
        pc_df_norm = pc_df[pc_cols].copy()

        # Normalizasyon (0-1 arası)
        pc_df_norm = (pc_df_norm - pc_df_norm.min()) / (pc_df_norm.max() - pc_df_norm.min())
        pc_df_norm["Name"] = pc_df["Name"].values

        fig_pc = px.parallel_coordinates(
            pc_df_norm,
            dimensions=pc_cols,
            color="Global_Sales",
            color_continuous_scale=px.colors.sequential.Viridis,
            labels={col: col for col in pc_cols},
            title="Parallel Coordinates of Regional vs Global Sales (Top Games)"
        )
        st.plotly_chart(fig_pc, use_container_width=True)

        # 7) Correlation Heatmap (sales kolonları arası ilişki)
        st.markdown("#### Correlation Heatmap: Sales Variables")

        corr_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales", "Total_Regional_Sales"]
        corr_df = filtered_df[corr_cols].corr()

        fig_heatmap = px.imshow(
            corr_df,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap of Sales Columns",
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # 8) Scatter Matrix: çok boyutlu satış ilişkileri
        st.markdown("#### Scatter Matrix: Regional Sales Relationships")

        sm_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
        sm_source = filtered_df[["Genre"] + sm_cols].dropna()

        if sm_source.empty:
            st.info("Scatter matrix için yeterli veri bulunamadı.")
        else:
            sm_sample = sm_source.sample(min(400, len(sm_source)), random_state=42)
            fig_scatter_matrix = px.scatter_matrix(
                sm_sample,
                dimensions=sm_cols,
                color="Genre",
                title="Scatter Matrix of Regional and Global Sales",
                height=900,
                width=900,
                opacity=0.75,
            )
            fig_scatter_matrix.update_layout(dragmode="select")
            fig_scatter_matrix.for_each_xaxis(lambda ax: ax.update(side="bottom"))
            st.plotly_chart(fig_scatter_matrix, use_container_width=True)

        # 9) Sunburst: Genre → Platform hiyerarşisi
        st.markdown("#### Sunburst: Genre → Platform Sales Structure")

        sunburst_df = (
            filtered_df.groupby(["Genre", "Platform"], as_index=False)["Global_Sales"]
            .sum()
        )

        fig_sunburst = px.sunburst(
            sunburst_df,
            path=["Genre", "Platform"],
            values="Global_Sales",
            title="Sunburst of Global Sales by Genre and Platform",
        )
        fig_sunburst.update_layout(width=900, height=700)
        st.plotly_chart(fig_sunburst, use_container_width=True)


if __name__ == "__main__":
    main()
