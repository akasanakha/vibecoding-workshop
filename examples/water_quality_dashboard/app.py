"""
💧 Water Quality Dashboard
===========================
A synthetic water quality monitoring dashboard with interactive maps,
time series, station comparisons, and correlation heatmaps.
Students learn: synthetic data generation, maps, time series, heatmaps.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="💧 Water Quality Dashboard",
    page_icon="💧",
    layout="wide",
)

# ── Generate Synthetic Data ─────────────────────────────────────────────────
# We create realistic-looking water quality data inline so no external file
# is needed. Each station has GPS coordinates and daily measurements.

@st.cache_data
def generate_data():
    np.random.seed(42)

    # Define monitoring stations with real-ish Manitoba lake coordinates
    stations = {
        "Station A - Lake Winnipeg North": (52.50, -96.90),
        "Station B - Lake Winnipeg South": (50.50, -96.70),
        "Station C - Lake Manitoba": (50.80, -98.70),
        "Station D - Cedar Lake": (53.30, -99.80),
        "Station E - Playgreen Lake": (53.70, -97.80),
        "Station F - Dauphin Lake": (51.20, -99.90),
    }

    dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
    rows = []

    for name, (lat, lon) in stations.items():
        n = len(dates)
        # Seasonal component (warmer in summer)
        day_of_year = np.arange(n) % 365
        seasonal = np.sin(2 * np.pi * day_of_year / 365)

        rows.append(pd.DataFrame({
            "Station": name,
            "Date": dates[:n],
            "Latitude": lat,
            "Longitude": lon,
            # Temperature: ~0°C winter, ~22°C summer + noise
            "Temperature (°C)": np.round(11 + 11 * seasonal + np.random.normal(0, 1.5, n), 1),
            # Dissolved oxygen inversely related to temperature
            "Dissolved O₂ (mg/L)": np.round(10 - 2 * seasonal + np.random.normal(0, 0.8, n), 1),
            # pH: relatively stable 7-9
            "pH": np.round(8.0 + 0.3 * seasonal + np.random.normal(0, 0.2, n), 2),
            # Turbidity: higher in spring runoff
            "Turbidity (NTU)": np.round(
                np.clip(15 + 10 * np.sin(2 * np.pi * (day_of_year - 90) / 365)
                        + np.random.exponential(3, n), 1, 80), 1
            ),
            # Chlorophyll-a: peaks in summer (algae bloom)
            "Chlorophyll-a (µg/L)": np.round(
                np.clip(5 + 8 * np.clip(seasonal, 0, 1) + np.random.exponential(2, n), 0.5, 40), 1
            ),
        }))

    return pd.concat(rows, ignore_index=True)

df = generate_data()
parameters = ["Temperature (°C)", "Dissolved O₂ (mg/L)", "pH", "Turbidity (NTU)", "Chlorophyll-a (µg/L)"]

# ── Header ──────────────────────────────────────────────────────────────────
st.title("💧 Water Quality Dashboard")
st.markdown(
    "Monitor water quality across **six synthetic monitoring stations** in "
    "Manitoba. Explore spatial patterns, seasonal trends, and parameter "
    "correlations. Data is generated programmatically to illustrate common "
    "limnological patterns."
)
st.divider()

# ── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Controls")

all_stations = sorted(df["Station"].unique())
selected_stations = st.sidebar.multiselect(
    "Stations", all_stations, default=all_stations
)

date_range = st.sidebar.date_input(
    "Date range",
    value=(df["Date"].min(), df["Date"].max()),
    min_value=df["Date"].min(),
    max_value=df["Date"].max(),
)

# Handle single-date selection gracefully
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0] if isinstance(date_range, (list, tuple)) else date_range

filtered = df[
    df["Station"].isin(selected_stations)
    & (df["Date"] >= pd.Timestamp(start_date))
    & (df["Date"] <= pd.Timestamp(end_date))
].copy()

st.sidebar.metric("Records", f"{len(filtered):,}")

# ── Key Metrics ─────────────────────────────────────────────────────────────
if not filtered.empty:
    cols = st.columns(5)
    for i, param in enumerate(parameters):
        cols[i].metric(param.split("(")[0].strip(), f"{filtered[param].mean():.1f}")

# ── Tabs ────────────────────────────────────────────────────────────────────
tab_map, tab_ts, tab_compare, tab_corr = st.tabs(
    ["🗺️ Station Map", "📈 Time Series", "⚖️ Station Comparison", "🔥 Correlation Heatmap"]
)

# ── Tab 1: Map ──────────────────────────────────────────────────────────────
with tab_map:
    if filtered.empty:
        st.warning("No data for current selection.")
    else:
        st.subheader("Monitoring Station Locations")
        # Get one row per station for the map
        map_df = (
            filtered.groupby("Station")
            .agg({"Latitude": "first", "Longitude": "first", "Temperature (°C)": "mean"})
            .reset_index()
            .rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
        )
        st.map(map_df, latitude="latitude", longitude="longitude", size=50000)
        st.caption("Bubble locations represent station coordinates. Zoom and pan to explore.")

# ── Tab 2: Time Series ─────────────────────────────────────────────────────
with tab_ts:
    if filtered.empty:
        st.warning("No data for current selection.")
    else:
        param = st.selectbox("Parameter", parameters, key="ts_param")
        # Resample to weekly means for smoother lines
        ts = (
            filtered.groupby(["Station", pd.Grouper(key="Date", freq="W")])[param]
            .mean()
            .reset_index()
        )
        fig = px.line(
            ts, x="Date", y=param, color="Station",
            template="plotly_white",
        )
        fig.update_layout(margin=dict(t=10, b=10), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 3: Station Comparison ──────────────────────────────────────────────
with tab_compare:
    if filtered.empty:
        st.warning("No data for current selection.")
    else:
        param2 = st.selectbox("Parameter", parameters, key="cmp_param")
        fig_box = px.box(
            filtered, x="Station", y=param2, color="Station",
            template="plotly_white",
        )
        fig_box.update_layout(
            margin=dict(t=10, b=10),
            showlegend=False,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ── Tab 4: Correlation Heatmap ──────────────────────────────────────────────
with tab_corr:
    if filtered.empty:
        st.warning("No data for current selection.")
    else:
        st.subheader("Parameter Correlation Matrix")
        corr = filtered[parameters].corr().round(2)
        fig_heat = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            template="plotly_white",
        )
        fig_heat.update_layout(margin=dict(t=10, b=10), height=500)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption(
            "Strong negative correlation between Temperature and Dissolved O₂ "
            "reflects the physical relationship: warmer water holds less oxygen."
        )

# ── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Data: Synthetically generated for educational purposes · "
    "Built with Streamlit + Plotly + NumPy"
)
