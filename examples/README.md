# 🌿 Vibecoding Workshop — Example Streamlit Apps

Three complete, deployable Streamlit dashboards designed for ecology students learning to build interactive data tools with Python.

---

## Quick Start

Each example is self-contained. To run any app:

```bash
cd examples/<app_folder>
pip install -r requirements.txt
streamlit run app.py
```

---

## 🐧 Example 1: Biodiversity Explorer

**Folder:** `biodiversity_explorer/`

Explore morphological measurements of three penguin species from the Palmer Archipelago, Antarctica.

### What It Looks Like
- **Sidebar** with species, island, and sex filters
- **Metric cards** showing count, species, avg body mass, avg flipper length
- **Scatter plots** (bill length vs depth, flipper length vs body mass) colored by species
- **Distribution histograms** for any measurement, overlaid by species
- **Summary statistics table** with full descriptive stats grouped by species

### Dataset
[Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) — 344 observations of Adélie, Chinstrap, and Gentoo penguins.

### What Students Learn
- Loading CSV data from a URL with `pd.read_csv()`
- Using `@st.cache_data` to avoid re-downloading
- Building sidebar filters with `st.multiselect`
- Creating scatter plots and histograms with Plotly Express
- Organizing content with `st.tabs()` and `st.columns()`
- Handling missing data with `.dropna()`

---

## 💧 Example 2: Water Quality Dashboard

**Folder:** `water_quality_dashboard/`

Monitor water quality across six synthetic monitoring stations, with maps, time series, and correlations.

### What It Looks Like
- **Interactive map** showing station locations across Manitoba lakes
- **Time series** of any parameter (temperature, dissolved oxygen, pH, turbidity, chlorophyll-a) with weekly smoothing
- **Box plots** comparing parameter distributions across stations
- **Correlation heatmap** revealing relationships between parameters (e.g., temperature vs dissolved oxygen)

### Dataset
Synthetically generated inline using NumPy — realistic seasonal patterns for 6 stations over 2 years.

### What Students Learn
- Generating realistic synthetic ecological data with NumPy
- Adding seasonal/cyclical patterns with `np.sin()`
- Displaying maps with `st.map()`
- Building time series with `pd.Grouper` for resampling
- Creating correlation heatmaps with `px.imshow()`
- Using date range inputs in the sidebar

---

## 🦅 Example 3: Species Impact Analyzer

**Folder:** `species_impact_analyzer/`

Analyze FAA wildlife strike reports at US airports — spatial patterns, seasonal trends, and species breakdowns.

### What It Looks Like
- **Summary metrics** — total incidents, unique species, airports affected, damage rate
- **Scatter map** of incident locations across the US (sampled for performance)
- **Timeline** showing incidents by year and monthly seasonality
- **Top species bar chart** with damage severity breakdown
- **Filterable data table** for raw exploration

### Dataset
[FAA Wildlife Strikes](https://wildlife.faa.gov/) via [TidyTuesday](https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-07-23) — ~56,000 strike records.

### What Students Learn
- Working with large real-world datasets (56K+ rows)
- Data cleaning: parsing dates, filling NAs, type coercion
- Performance optimization: sampling large datasets for maps
- Building interactive maps with `px.scatter_map()`
- Stacked bar charts for categorical breakdowns
- Slider and multiselect filters for dynamic exploration

---

## 🛠️ Common Patterns Across All Apps

| Pattern | Where to Find It |
|---|---|
| `st.set_page_config()` | Top of every app |
| `@st.cache_data` | Data loading functions |
| `st.sidebar` filters | All three apps |
| `st.tabs()` for organization | All three apps |
| `st.columns()` for layout | Metrics rows, scatter plots |
| `st.metric()` cards | All three apps |
| Plotly Express charts | All three apps |
| Graceful missing data handling | `.dropna()`, `.fillna()`, warnings |

---

## 📦 Tech Stack

- **[Streamlit](https://streamlit.io/)** — UI framework
- **[Pandas](https://pandas.pydata.org/)** — data manipulation
- **[Plotly](https://plotly.com/python/)** — interactive visualizations
- **[NumPy](https://numpy.org/)** — synthetic data generation (Water Quality only)

---

*Built for the Vibecoding Workshop · 2026*
