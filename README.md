# Space Missions Dashboard

Interactive dashboard to visualize and analyze historical space mission data from 1957 onwards, built with **Python** and **Streamlit**.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure `space_missions.csv` is in the project root directory.

## Project Structure

| File | Description |
|---|---|
| `app.py` | Streamlit dashboard with filters, KPIs, charts, and data table |
| `space_missions.py` | 8 grading functions for programmatic testing |
| `requirements.txt` | Python dependencies |

## Visualization Choices

### 1. Missions Per Year — Line Chart
A line chart is the standard choice for time-series data. It clearly reveals long-term trends such as the Cold War space-race peak in the 1960s–70s, the dip in the 1990s after the Soviet Union dissolved, and the recent surge driven by commercial launch providers like SpaceX. Markers on each data point make individual years easy to inspect via hover.

### 2. Mission Status Distribution — Donut Chart
A donut chart is effective for showing proportions of a categorical whole. With only 4 possible statuses (Success, Failure, Partial Failure, Prelaunch Failure), the chart remains easy to read at a glance and immediately communicates that the vast majority of missions succeed.

### 3. Top 10 Companies by Mission Count — Horizontal Bar Chart
A horizontal bar chart is the best way to rank categorical items when the labels are long text strings (company names). Sorting bars by length makes comparison instant, and the horizontal orientation keeps labels fully legible without rotation.

### 4. Success Rate by Top 10 Companies — Bar Chart with Color Scale
Comparing success rates across companies answers "who is the most reliable?" A vertical bar chart with a continuous green color scale ties visual intensity to the metric. Hover data includes total mission count so viewers can judge statistical significance — a 100% success rate from 2 launches is less meaningful than 90% from 500.

### 5. Top 10 Most Used Rockets — Horizontal Bar Chart
Identifying the most-used rocket models complements the company view. A horizontal bar chart handles long rocket model names well (e.g., "Cosmos-3M (11K65M)"), and sorted bars allow quick comparison of launch frequencies across different rocket platforms.
