# Vibecoding Cheat Sheet

## The Golden Rules

1. **Be specific.** "Make a chart" → "Make a bar chart showing species count by habitat type"
2. **Go step by step.** Don't ask for the whole app at once. Build one feature at a time.
3. **Show, don't tell.** Paste in your data structure. Paste in error messages. Give context.
4. **Iterate.** First version won't be perfect. Say what's wrong and ask for changes.
5. **Ask why.** "Explain what this code does" is always a valid prompt.

## Prompt Templates

### Starting a new project
```
I want to build a web app using Streamlit (Python) that:
- Loads a CSV dataset about [topic]
- Shows [specific visualization]
- Lets users [specific interaction]
The dataset has columns: [list columns]
Let's start with loading and displaying the data.
```

### Adding a visualization
```
Add a [chart type] that shows [what to plot].
X-axis: [column name]
Y-axis: [column name]
Color by: [column name]
Use plotly for interactive charts.
```

### Adding interactivity
```
Add a sidebar with:
- A dropdown to filter by [column]
- A slider to set the range for [column]
- A text search box for [column]
The visualizations should update when filters change.
```

### Adding a map
```
Add an interactive map showing [what].
The data has latitude in column [name] and longitude in column [name].
Color the points by [column].
Add popups showing [details] when you click a point.
```

### Fixing errors
```
I'm getting this error:
[paste the full error message]

Here's the relevant code:
[paste the code section]

What's wrong and how do I fix it?
```

### Making it look better
```
Improve the layout:
- Add a title and description at the top
- Organize into tabs: [tab1], [tab2], [tab3]
- Use a clean color scheme
- Add units and labels to all charts
```

## Common Streamlit Patterns

```python
# Basic app structure
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="My App", layout="wide")
st.title("My Ecology App")

# Load data
df = pd.read_csv("data.csv")

# Sidebar filters
species = st.sidebar.multiselect("Species", df["species"].unique())

# Filter data
if species:
    df = df[df["species"].isin(species)]

# Visualize
fig = px.scatter(df, x="longitude", y="latitude", color="species")
st.plotly_chart(fig, use_container_width=True)
```

## Deployment Quick Steps

### Streamlit Cloud
1. Push code to GitHub
2. Go to share.streamlit.io
3. Point to your repo and main file
4. Click Deploy

### Vercel
1. Push code to GitHub
2. Go to vercel.com/new
3. Import your repo
4. Click Deploy

## When You're Stuck
1. Copy the exact error message
2. Tell the AI what you were trying to do
3. Paste the relevant code
4. Ask it to fix the issue and explain what went wrong
