"""
🦅 Species Impact Analyzer - Wildlife Strikes Dashboard
========================================================
Explore FAA wildlife strike data at US airports.
Students learn: large dataset handling, maps, bar charts, timelines, metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="🦅 Species Impact Analyzer",
    page_icon="🦅",
    layout="wide",
)

# ── Load Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-23/wildlife_impacts.csv"
    df = pd.read_csv(url, low_memory=False)

    # Parse date column
    df["incident_date"] = pd.to_datetime(df["incident_date"], errors="coerce")
    df["year"] = df["incident_date"].dt.year

    # Clean species names: fill blanks, title-case
    df["species"] = df["species"].fillna("Unknown").str.strip().str.title()

    # Clean airport names
    df["airport"] = df["airport"].fillna("Unknown")

    # Ensure numeric coordinates
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")

    return df

df = load_data()

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🦅 Species Impact Analyzer")
st.markdown(
    "Analyze **FAA wildlife strike reports** at US airports. Filter by "
    "species and airport to discover spatial and temporal patterns in "
    "wildlife–aircraft collisions. Data from "
    "[TidyTuesday](https://github.com/rfordatascience/tidytuesday)."
)
st.divider()

# ── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

# Year range slider
min_year = int(df["year"].min()) if df["year"].notna().any() else 1990
max_year = int(df["year"].max()) if df["year"].notna().any() else 2020
year_range = st.sidebar.slider(
    "Year range", min_year, max_year, (min_year, max_year)
)

# Top species for the multiselect (show most common)
top_species = df["species"].value_counts().head(30).index.tolist()
selected_species = st.sidebar.multiselect(
    "Species (top 30 shown)", top_species, default=[]
)

# Top airports
top_airports = df["airport"].value_counts().head(30).index.tolist()
selected_airports = st.sidebar.multiselect(
    "Airport (top 30 shown)", top_airports, default=[]
)

# Apply filters
filtered = df[
    (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])
].copy()

if selected_species:
    filtered = filtered[filtered["species"].isin(selected_species)]
if selected_airports:
    filtered = filtered[filtered["airport"].isin(selected_airports)]

st.sidebar.markdown("---")
st.sidebar.metric("Incidents shown", f"{len(filtered):,} / {len(df):,}")

# ── Summary Metrics ─────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Incidents", f"{len(filtered):,}")
m2.metric("Unique Species", f"{filtered['species'].nunique():,}")
m3.metric("Airports Affected", f"{filtered['airport'].nunique():,}")
damage_pct = (
    (filtered["damage"].isin(["Substantial", "Destroyed"]).sum() / len(filtered) * 100)
    if len(filtered) else 0
)
m4.metric("Substantial+ Damage", f"{damage_pct:.1f}%")

# ── Tabs ────────────────────────────────────────────────────────────────────
tab_map, tab_timeline, tab_species, tab_data = st.tabs(
    ["🗺️ Incident Map", "📈 Timeline", "🐦 Top Species", "📋 Data"]
)

# ── Tab 1: Map ──────────────────────────────────────────────────────────────
with tab_map:
    # Only plot rows that have valid coordinates
    map_df = filtered.dropna(subset=["latitude", "longitude"]).copy()

    if map_df.empty:
        st.info("No geolocated incidents for the current selection.")
    else:
        st.subheader("Incident Locations")
        # Sample if too many points for performance
        if len(map_df) > 5000:
            map_sample = map_df.sample(5000, random_state=42)
            st.caption(f"Showing 5,000 of {len(map_df):,} incidents (sampled for performance).")
        else:
            map_sample = map_df

        fig_map = px.scatter_map(
            map_sample,
            lat="latitude",
            lon="longitude",
            color="species" if len(map_sample["species"].unique()) <= 15 else None,
            hover_name="species",
            hover_data=["airport", "incident_date"],
            zoom=3,
            center={"lat": 39, "lon": -97},
            opacity=0.5,
            height=550,
        )
        fig_map.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_map, use_container_width=True)

# ── Tab 2: Timeline ────────────────────────────────────────────────────────
with tab_timeline:
    if filtered.empty:
        st.warning("No data for current selection.")
    else:
        st.subheader("Incidents Over Time")
        # Group by year
        yearly = filtered.groupby("year").size().reset_index(name="Incidents")
        fig_line = px.bar(
            yearly, x="year", y="Incidents",
            template="plotly_white",
            labels={"year": "Year"},
        )
        fig_line.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig_line, use_container_width=True)

        # Monthly seasonality
        st.subheader("Monthly Seasonality")
        filtered["month"] = filtered["incident_date"].dt.month
        monthly = filtered.dropna(subset=["month"]).groupby("month").size().reset_index(name="Incidents")
        monthly["Month Name"] = monthly["month"].apply(
            lambda m: ["Jan","Feb","Mar","Apr","May","Jun",
                        "Jul","Aug","Sep","Oct","Nov","Dec"][int(m)-1]
        )
        fig_month = px.bar(
            monthly, x="Month Name", y="Incidents",
            template="plotly_white",
        )
        fig_month.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig_month, use_container_width=True)

# ── Tab 3: Top Species ─────────────────────────────────────────────────────
with tab_species:
    if filtered.empty:
        st.warning("No data for current selection.")
    else:
        n_top = st.slider("Number of top species", 5, 30, 15)
        top = filtered["species"].value_counts().head(n_top).reset_index()
        top.columns = ["Species", "Count"]

        fig_bar = px.bar(
            top, x="Count", y="Species", orientation="h",
            template="plotly_white",
            color="Count",
            color_continuous_scale="YlOrRd",
        )
        fig_bar.update_layout(
            margin=dict(t=10, b=10),
            yaxis=dict(autorange="reversed"),
            height=max(400, n_top * 28),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Damage breakdown for top species
        st.subheader("Damage Severity by Top Species")
        top_species_list = top["Species"].tolist()
        damage_df = filtered[filtered["species"].isin(top_species_list)].copy()
        damage_df["damage"] = damage_df["damage"].fillna("None")
        damage_counts = damage_df.groupby(["species", "damage"]).size().reset_index(name="Count")

        fig_stack = px.bar(
            damage_counts, x="species", y="Count", color="damage",
            template="plotly_white",
            category_orders={"damage": ["None", "Minor", "Uncertain", "Substantial", "Destroyed"]},
        )
        fig_stack.update_layout(
            margin=dict(t=10, b=10),
            xaxis_tickangle=-40,
        )
        st.plotly_chart(fig_stack, use_container_width=True)

# ── Tab 4: Raw Data ────────────────────────────────────────────────────────
with tab_data:
    st.subheader("Filtered Dataset")
    display_cols = [
        "incident_date", "airport", "species", "damage",
        "num_engs", "latitude", "longitude", "state",
    ]
    available_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[available_cols].head(500),
        use_container_width=True,
        height=400,
    )
    st.caption("Showing first 500 rows. Apply filters to narrow the view.")

# ── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Data: [FAA Wildlife Strike Database](https://wildlife.faa.gov/) via "
    "[TidyTuesday](https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-07-23) · "
    "Built with Streamlit + Plotly"
)
