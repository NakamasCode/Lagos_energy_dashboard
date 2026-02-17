import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Lagos Energy Dashboard")

# Load data
master = pd.read_csv("master_clean.csv")
master['MONTH'] = pd.to_datetime(master['MONTH'])

# Year filter
year_selected = st.selectbox("Select Year", master['YEAR'].unique())
master_filtered = master[master['YEAR'] == year_selected]

# --- 1. Total Energy (Discos only) ---
st.subheader(f"Monthly Energy Delivered per Disco ({year_selected})")

fig_total_disco = px.line(
    master_filtered,
    x="MONTH",
    y=["EKO_TOTAL", "IKEJA_TOTAL"],
    labels={"value": "Energy (MWh)", "variable": "Disco"},
    markers=True
)
st.plotly_chart(fig_total_disco, use_container_width=True)

# --- 2. Average Energy (Discos only) ---
st.subheader(f"Monthly Average Energy per Disco ({year_selected})")

fig_avg_disco = px.line(
    master_filtered,
    x="MONTH",
    y=["EKO_AVG", "IKEJA_AVG"],
    labels={"value": "Average Energy", "variable": "Disco"},
    markers=True
)
st.plotly_chart(fig_avg_disco, use_container_width=True)

# --- 3. Total Energy (All Discos) ---
st.subheader(f"Monthly Total Energy ({year_selected})")

fig_total_all = px.line(
    master_filtered,
    x="MONTH",
    y=["LAGOS_TOTAL"],   # only total
    labels={"TOTAL_TOTAL": "Total Energy (MWh)"},
    markers=True
)
st.plotly_chart(fig_total_all, use_container_width=True)

# --- 4. Average Energy (All Discos) ---
st.subheader(f"Monthly Average Energy ({year_selected})")

fig_avg_all = px.line(
    master_filtered,
    x="MONTH",
    y=["LAGOS_AVG"],   # only average total
    labels={"AVG_TOTAL": "Average Energy"},
    markers=True
)
st.plotly_chart(fig_avg_all, use_container_width=True)
