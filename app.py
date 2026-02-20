import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title("Lagos Energy Dashboard")

# --- Load data ---
master = pd.read_csv("master_clean.csv")
master['MONTH'] = pd.to_datetime(master['MONTH'])

# --- Year selection (up to 3 years) ---
years_selected = st.multiselect(
    "Select up to 3 years to compare",
    options=master['YEAR'].unique(),
    default=master['YEAR'].sort_values(ascending=False)[:3]
)

if not years_selected:
    st.warning("Please select at least one year to view the dashboard.")
    st.stop()

master_filtered = master[master['YEAR'].isin(years_selected)]

# --- Function to find peak and lowest month for a column ---
def add_peak_low_annotations(fig, df, y_col, disco_name=None):
    for year in df['YEAR'].unique():
        year_df = df[df['YEAR'] == year]
        # Max
        max_row = year_df.loc[year_df[y_col].idxmax()]
        fig.add_trace(go.Scatter(
            x=[max_row['MONTH']],
            y=[max_row[y_col]],
            mode='markers+text',
            marker=dict(color='green', size=12),
            text=[f"Peak {year}" if not disco_name else f"{disco_name} Peak {year}"],
            textposition="top center",
            showlegend=False
        ))
        # Min
        min_row = year_df.loc[year_df[y_col].idxmin()]
        fig.add_trace(go.Scatter(
            x=[min_row['MONTH']],
            y=[min_row[y_col]],
            mode='markers+text',
            marker=dict(color='red', size=12),
            text=[f"Lowest {year}" if not disco_name else f"{disco_name} Lowest {year}"],
            textposition="bottom center",
            showlegend=False
        ))

# --- 1. Total Energy per Disco ---
st.subheader(f"Monthly Energy Delivered per Disco ({', '.join(map(str, years_selected))})")
fig_total_disco = px.line(
    master_filtered,
    x="MONTH",
    y=["EKO_TOTAL", "IKEJA_TOTAL"],
    color='YEAR',
    line_dash='variable',
    labels={"value": "Energy (MWh)", "variable": "Disco", "YEAR": "Year"},
    markers=True
)
# Add peak/low markers
for disco in ["EKO_TOTAL", "IKEJA_TOTAL"]:
    add_peak_low_annotations(fig_total_disco, master_filtered, disco, disco_name=disco)
st.plotly_chart(fig_total_disco, use_container_width=True)

# --- 2. Average Energy per Disco ---
st.subheader(f"Monthly Average Energy per Disco ({', '.join(map(str, years_selected))})")
fig_avg_disco = px.line(
    master_filtered,
    x="MONTH",
    y=["EKO_AVG", "IKEJA_AVG"],
    color='YEAR',
    line_dash='variable',
    labels={"value": "Average Energy", "variable": "Disco", "YEAR": "Year"},
    markers=True
)
for disco in ["EKO_AVG", "IKEJA_AVG"]:
    add_peak_low_annotations(fig_avg_disco, master_filtered, disco, disco_name=disco)
st.plotly_chart(fig_avg_disco, use_container_width=True)

# --- 3. Total Energy (All Discos) ---
st.subheader(f"Monthly Total Energy ({', '.join(map(str, years_selected))})")
fig_total_all = px.line(
    master_filtered,
    x="MONTH",
    y=["LAGOS_TOTAL"],
    color='YEAR',
    labels={"value": "Total Energy (MWh)", "YEAR": "Year"},
    markers=True
)
add_peak_low_annotations(fig_total_all, master_filtered, "LAGOS_TOTAL")
st.plotly_chart(fig_total_all, use_container_width=True)

# --- 4. Average Energy (All Discos) ---
st.subheader(f"Monthly Average Energy ({', '.join(map(str, years_selected))})")
fig_avg_all = px.line(
    master_filtered,
    x="MONTH",
    y=["LAGOS_AVG"],
    color='YEAR',
    labels={"value": "Average Energy", "YEAR": "Year"},
    markers=True
)
add_peak_low_annotations(fig_avg_all, master_filtered, "LAGOS_AVG")
st.plotly_chart(fig_avg_all, use_container_width=True)