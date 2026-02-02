"""
🐧 Biodiversity Explorer - Palmer Penguins Dashboard
=====================================================
An interactive dashboard for exploring the Palmer Penguins dataset.
Students learn: data loading, filtering, scatter plots, histograms, summary stats.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐧 Biodiversity Explorer",
    page_icon="🐧",
    layout="wide",
)

# ── Load Data ───────────────────────────────────────────────────────────────
# Cache the data so it only downloads once per session
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
    df = pd.read_csv(url)
    # Clean column names for display
    df.columns = df.columns.str.replace("_", " ").str.title()
    return df

df = load_data()

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🐧 Biodiversity Explorer")
st.markdown(
    "Explore morphological measurements of **Adélie**, **Chinstrap**, and "
    "**Gentoo** penguins observed on three islands in the Palmer Archipelago, "
    "Antarctica. Use the sidebar filters to focus on subsets of the data."
)
st.divider()

# ── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

# Species filter
all_species = sorted(df["Species"].dropna().unique())
selected_species = st.sidebar.multiselect(
    "Species", all_species, default=all_species
)

# Island filter
all_islands = sorted(df["Island"].dropna().unique())
selected_islands = st.sidebar.multiselect(
    "Island", all_islands, default=all_islands
)

# Sex filter
all_sex = sorted(df["Sex"].dropna().unique())
selected_sex = st.sidebar.multiselect(
    "Sex", all_sex, default=all_sex
)

# Apply filters (handle missing values gracefully)
mask = (
    df["Species"].isin(selected_species)
    & df["Island"].isin(selected_islands)
    & df["Sex"].isin(selected_sex)
)
filtered = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Penguins shown", f"{len(filtered)} / {len(df)}")

# ── Key Metrics Row ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penguins", len(filtered))
col2.metric("Species", filtered["Species"].nunique())
col3.metric("Avg Body Mass (g)", f"{filtered['Body Mass G'].mean():.0f}" if len(filtered) else "—")
col4.metric("Avg Flipper (mm)", f"{filtered['Flipper Length Mm'].mean():.1f}" if len(filtered) else "—")

# ── Tabs for Visualizations ─────────────────────────────────────────────────
tab_scatter, tab_hist, tab_stats = st.tabs(
    ["📈 Scatter Plots", "📊 Distributions", "📋 Summary Statistics"]
)

# Color palette consistent across all plots
color_map = {"Adelie": "#ff6f61", "Chinstrap": "#6b5b95", "Gentoo": "#88b04b"}

# ── Tab 1: Scatter Plots ────────────────────────────────────────────────────
with tab_scatter:
    if filtered.empty:
        st.warning("No data matches the current filters.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Bill Length vs Bill Depth")
            fig1 = px.scatter(
                filtered.dropna(subset=["Bill Length Mm", "Bill Depth Mm"]),
                x="Bill Length Mm",
                y="Bill Depth Mm",
                color="Species",
                color_discrete_map=color_map,
                hover_data=["Island", "Sex"],
                opacity=0.7,
                template="plotly_white",
            )
            fig1.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("Flipper Length vs Body Mass")
            fig2 = px.scatter(
                filtered.dropna(subset=["Flipper Length Mm", "Body Mass G"]),
                x="Flipper Length Mm",
                y="Body Mass G",
                color="Species",
                color_discrete_map=color_map,
                hover_data=["Island", "Sex"],
                opacity=0.7,
                template="plotly_white",
            )
            fig2.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)

# ── Tab 2: Distribution Histograms ──────────────────────────────────────────
with tab_hist:
    if filtered.empty:
        st.warning("No data matches the current filters.")
    else:
        measure = st.selectbox(
            "Select measurement",
            ["Bill Length Mm", "Bill Depth Mm", "Flipper Length Mm", "Body Mass G"],
        )
        fig3 = px.histogram(
            filtered.dropna(subset=[measure]),
            x=measure,
            color="Species",
            color_discrete_map=color_map,
            barmode="overlay",
            opacity=0.7,
            nbins=30,
            template="plotly_white",
        )
        fig3.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig3, use_container_width=True)

# ── Tab 3: Summary Statistics ────────────────────────────────────────────────
with tab_stats:
    if filtered.empty:
        st.warning("No data matches the current filters.")
    else:
        numeric_cols = ["Bill Length Mm", "Bill Depth Mm", "Flipper Length Mm", "Body Mass G"]
        summary = (
            filtered.groupby("Species")[numeric_cols]
            .describe()
            .round(1)
        )
        st.dataframe(summary, use_container_width=True)

        st.subheader("Filtered Data Preview")
        st.dataframe(filtered, use_container_width=True, height=300)

# ── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Data: [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) "
    "by Allison Horst, Alison Hill & Kristen Gorman · "
    "Built with Streamlit + Plotly"
)
