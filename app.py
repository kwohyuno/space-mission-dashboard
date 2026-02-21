import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Space Missions Dashboard", page_icon="\U0001F680", layout="wide", menu_items={})

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "space_missions.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = df["Date"].dt.year.astype("Int64")
    return df


df = load_data()

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("\U0001F680 Space Missions Dashboard")
st.markdown("Interactive exploration of every orbital launch from **1957** onwards.")

# ---------------------------------------------------------------------------
# Sidebar – interactive filters
# ---------------------------------------------------------------------------
st.sidebar.header("Filters")

# Year range
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())
year_range = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))

# Company
all_companies = sorted(df["Company"].unique().tolist())
selected_companies = st.sidebar.multiselect("Company", all_companies, default=[])

# Mission status
all_statuses = sorted(df["MissionStatus"].dropna().unique().tolist())
selected_statuses = st.sidebar.multiselect("Mission Status", all_statuses, default=[])

# Rocket status
all_rocket_statuses = sorted(df["RocketStatus"].dropna().unique().tolist())
selected_rocket_status = st.sidebar.multiselect("Rocket Status", all_rocket_statuses, default=[])

# Apply filters
filtered = df.copy()
filtered = filtered[(filtered["Year"] >= year_range[0]) & (filtered["Year"] <= year_range[1])]
if selected_companies:
    filtered = filtered[filtered["Company"].isin(selected_companies)]
if selected_statuses:
    filtered = filtered[filtered["MissionStatus"].isin(selected_statuses)]
if selected_rocket_status:
    filtered = filtered[filtered["RocketStatus"].isin(selected_rocket_status)]

# ---------------------------------------------------------------------------
# Summary statistics (KPIs)
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
total = len(filtered)
successes = int((filtered["MissionStatus"] == "Success").sum())
rate = round(successes / total * 100, 2) if total > 0 else 0.0
unique_companies = filtered["Company"].nunique()
unique_rockets = filtered["Rocket"].nunique()

col1.metric("Total Missions", f"{total:,}")
col2.metric("Success Rate", f"{rate}%")
col3.metric("Unique Companies", unique_companies)
col4.metric("Unique Rockets", unique_rockets)

st.divider()

# ---------------------------------------------------------------------------
# Visualization 1 – Missions Per Year  (Line Chart)
# ---------------------------------------------------------------------------
# WHY: A line chart is the standard choice for time-series data. It clearly
# reveals long-term trends such as the Cold War space-race peak, the dip in
# the 1990s after the Soviet Union dissolved, and the recent surge driven by
# commercial launch providers like SpaceX. Markers on each data point make
# individual years easy to inspect via hover.
# ---------------------------------------------------------------------------
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Missions Per Year")
    st.caption(
        "**Line chart** — ideal for time-series data. It reveals the Cold War peak, "
        "the 1990s decline, and the recent commercial-space surge."
    )
    yearly = filtered.groupby("Year").size().reset_index(name="Missions")
    fig1 = px.line(yearly, x="Year", y="Missions", markers=True)
    fig1.update_layout(height=400, margin=dict(t=10))
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------------------------
# Visualization 2 – Mission Status Distribution  (Donut Chart)
# ---------------------------------------------------------------------------
# WHY: A donut/pie chart is effective for showing proportions of a categorical
# whole. With only 4 possible statuses it is easy to read at a glance and
# immediately communicates that the vast majority of launches succeed.
# ---------------------------------------------------------------------------
with chart2:
    st.subheader("Mission Status Distribution")
    st.caption(
        "**Donut chart** — shows proportions of a whole at a glance. With only 4 "
        "status categories the chart stays readable and highlights overall success dominance."
    )
    status_counts = filtered["MissionStatus"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig2 = px.pie(status_counts, values="Count", names="Status", hole=0.4)
    fig2.update_layout(height=400, margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Visualization 3 – Top 10 Companies  (Horizontal Bar Chart)
# ---------------------------------------------------------------------------
# WHY: A horizontal bar chart is the best way to rank categorical items when
# the labels are long text strings (company names). Sorting bars by length
# makes comparison instant and the horizontal orientation keeps labels legible.
# ---------------------------------------------------------------------------
chart3, chart4 = st.columns(2)

with chart3:
    st.subheader("Top 10 Companies by Missions")
    st.caption(
        "**Horizontal bar chart** — perfect for ranking categories with long labels. "
        "Sorted bars make comparisons instant."
    )
    top_companies = filtered["Company"].value_counts().head(10).reset_index()
    top_companies.columns = ["Company", "Missions"]
    fig3 = px.bar(top_companies, x="Missions", y="Company", orientation="h")
    fig3.update_layout(height=400, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Visualization 4 – Success Rate by Top Companies  (Bar Chart with Color)
# ---------------------------------------------------------------------------
# WHY: Comparing success rates across companies answers "who is most
# reliable?" A vertical bar chart with a continuous green color scale ties
# visual intensity to the metric. Hover data includes total mission count so
# viewers can judge statistical significance (100% from 2 launches ≠ 90% from
# 500).
# ---------------------------------------------------------------------------
with chart4:
    st.subheader("Success Rate – Top 10 Companies")
    st.caption(
        "**Bar chart with color scale** — compares reliability across companies. "
        "Hover shows mission count for statistical context."
    )
    top10_names = filtered["Company"].value_counts().head(10).index.tolist()
    rates = []
    for c in top10_names:
        c_df = filtered[filtered["Company"] == c]
        s = int((c_df["MissionStatus"] == "Success").sum())
        rates.append({
            "Company": c,
            "Success Rate (%)": round(s / len(c_df) * 100, 2),
            "Total Missions": len(c_df),
        })
    rates_df = pd.DataFrame(rates)
    fig4 = px.bar(
        rates_df, x="Company", y="Success Rate (%)",
        hover_data=["Total Missions"],
        color="Success Rate (%)",
        color_continuous_scale="greens",
    )
    fig4.update_layout(height=400, margin=dict(t=10))
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------------------------
# Visualization 5 – Top 10 Rockets  (Horizontal Bar Chart)
# ---------------------------------------------------------------------------
# WHY: Identifying the most-used rocket models complements the company view.
# Again, a horizontal bar chart handles long rocket names well and sorted bars
# allow quick comparison of launch frequencies.
# ---------------------------------------------------------------------------
st.subheader("Top 10 Most Used Rockets")
st.caption(
    "**Horizontal bar chart** — highlights the workhorses of space exploration. "
    "Long rocket model names stay readable with horizontal orientation."
)
top_rockets = filtered["Rocket"].value_counts().head(10).reset_index()
top_rockets.columns = ["Rocket", "Launches"]
fig5 = px.bar(top_rockets, x="Launches", y="Rocket", orientation="h")
fig5.update_layout(height=400, margin=dict(t=10), yaxis=dict(autorange="reversed"))
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Data Table – sortable by clicking column headers
# ---------------------------------------------------------------------------
st.subheader("Mission Data")
st.caption("Click any column header to sort. Use the sidebar filters to narrow down results.")
display_cols = ["Company", "Location", "Date", "Rocket", "Mission", "RocketStatus", "Price", "MissionStatus"]
st.dataframe(filtered[display_cols], use_container_width=True, height=500)
