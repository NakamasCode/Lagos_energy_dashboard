import streamlit as st
import pandas as pd
import numpy as np
import random
import time

st.set_page_config(page_title="Grid Operations Dashboard", layout="wide")

st.title("⚡ Lagos Grid Operations Dashboard")

# -------------------------
# Simulated Real-Time Data
# -------------------------

generation = random.randint(4000, 5200)
demand = random.randint(4200, 5500)
frequency = round(random.uniform(49.7, 50.2), 2)

solar = random.randint(200, 400)
gas = random.randint(3000, 4200)
hydro = random.randint(600, 900)

# -------------------------
# Top Metrics
# -------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Generation (MW)", generation)
col2.metric("Total Demand (MW)", demand)
col3.metric("Grid Frequency (Hz)", frequency)

# Grid warning
if demand > generation:
    st.error("⚠ Demand exceeds generation. Possible load shedding.")
else:
    st.success("Grid operating normally")

st.divider()

# -------------------------
# Generation Mix
# -------------------------

st.subheader("Generation by Source")

gen_data = pd.DataFrame({
    "Source": ["Gas", "Hydro", "Solar"],
    "MW": [gas, hydro, solar]
})

st.bar_chart(gen_data.set_index("Source"))

# -------------------------
# Load vs Generation Curve
# -------------------------

st.subheader("Load vs Generation (24hr Trend)")

hours = np.arange(24)

load = np.random.randint(4200, 5500, size=24)
gen_curve = np.random.randint(4000, 5200, size=24)

trend_data = pd.DataFrame({
    "Load": load,
    "Generation": gen_curve
})

st.line_chart(trend_data)

# -------------------------
# Power Plant Status
# -------------------------

st.subheader("Power Plant Status")

plants = pd.DataFrame({
    "Plant": ["Egbin", "Geregu", "Olorunsogo"],
    "Capacity (MW)": [1320, 435, 750],
    "Status": ["Running", "Partial", "Offline"]
})

st.table(plants)

# -------------------------
# Auto Refresh
# -------------------------

time.sleep(5)
st.rerun()
