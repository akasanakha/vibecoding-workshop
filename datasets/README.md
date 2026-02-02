# Ecology & Biodiversity Datasets

Curated datasets for the vibecoding workshop. All are CSV format, ready for analysis and app-building.

---

## 1. 🐧 penguins.csv (344 rows, 16KB)
**Source:** [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) — Gorman, Williams & Fraser (2014)

**Columns:** species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex, year

**Description:** Body measurements for 3 penguin species (Adelie, Chinstrap, Gentoo) from 3 islands in the Palmer Archipelago, Antarctica.

**Project ideas:**
- Species classifier from body measurements
- Interactive visualization of morphological differences
- Statistical comparison dashboard across islands/years

---

## 2. 💧 water_quality.csv (1,672 rows, 136KB)
**Source:** Synthetic dataset modeled after Manitoba water monitoring stations

**Columns:** station_id, station_name, date, latitude, longitude, water_temp_c, ph, dissolved_oxygen_mg_l, total_nitrogen_mg_l, total_phosphorus_mg_l, chlorophyll_a_ug_l, secchi_depth_m

**Description:** Weekly water quality measurements from 8 stations across Manitoba (2019–2022) including Lake Winnipeg, Red River, and Assiniboine River. Features realistic seasonal patterns.

**Project ideas:**
- Water quality monitoring dashboard with map
- Seasonal trend analysis and forecasting
- Eutrophication risk indicator (nitrogen + phosphorus + chlorophyll)
- Station comparison tool

---

## 3. 🌱 threatened_plants.csv (500 rows, 56KB)
**Source:** [TidyTuesday 2020-08-18](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-08-18) — IUCN Red List of Threatened Species

**Columns:** binomial_name, country, continent, group, year_last_seen, threat_* (12 threat types), action_* (6 action types), red_list_category

**Description:** Extinct plant species worldwide with threat causes (agriculture, urbanization, climate change, etc.) and conservation actions taken.

**Project ideas:**
- Global extinction map by continent/country
- Threat analysis — which factors drive plant extinction?
- Conservation action effectiveness dashboard
- Timeline of species loss

---

## 4. 🌲 global_forest.csv (475 rows, 16KB)
**Source:** [TidyTuesday 2021-04-06](https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-04-06) — Our World in Data / UN FAO

**Columns:** entity, code, year, net_forest_conversion

**Description:** Net forest conversion (hectares/year) by country for 1990–2015. Positive = forest gain, negative = deforestation.

**Project ideas:**
- Deforestation leaderboard / ranking app
- Country comparison tool over time
- Regional trends visualization (link with world map)
- Correlation with economic indicators

---

## 5. 🦅 wildlife_impacts.csv (56,978 rows, 8.2MB)
**Source:** [TidyTuesday 2019-07-23](https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-07-23) — FAA Wildlife Strike Database

**Columns:** incident_date, state, airport_id, airport, operator, atype, type_eng, species_id, species, damage, num_engs, incident_month, incident_year, time_of_day, time, height, speed, phase_of_flt, sky, precip, cost_repairs_infl_adj

**Description:** Wildlife strikes with aircraft at US airports. Includes species identification, flight conditions, damage level, and repair costs.

**Project ideas:**
- Airport risk assessment dashboard
- Species hotspot map by state
- Seasonal/time-of-day pattern analysis
- Cost impact calculator
- Flight phase risk visualization

---

## 6. 🌡️ climate_canada.csv (528,278 rows, 23MB)
**Source:** [TidyTuesday 2020-01-07](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-07) — Australian Bureau of Meteorology / NASA GISS

**Columns:** city_name, date, temperature, temp_type, site_name

**Description:** Daily min/max temperature records for major global cities spanning over 100 years. Great for climate trend analysis.

**Project ideas:**
- Climate change visualization (temperature trends over decades)
- City temperature comparison tool
- Extreme weather event detector
- Heat wave frequency analysis
- Seasonal pattern explorer

---

## Quick Start

```python
import pandas as pd

# Load any dataset
df = pd.read_csv("penguins.csv")
print(df.head())
print(df.describe())
```
