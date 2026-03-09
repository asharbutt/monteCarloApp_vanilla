"""
Black-Scholes Pricer & Greeks Dashboard
========================================
Interactive Streamlit app for European option pricing and Greek analysis.

Run with:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vanilla_mc_sim as mc


# ── Page config ──
st.set_page_config(
    page_title="Black-Scholes Pricer",
    page_icon="📈",
    layout="wide",
)

st.title("Monte Carlo Simulator")
st.markdown("Vanilla European Option Pricer using MC")


# ══════════════════════════════════════════════════
# SIDEBAR: INPUT PARAMETERS
# ══════════════════════════════════════════════════

st.sidebar.header("Simulation Parameters")

S = st.sidebar.number_input("Spot Price (S)", value=100.0, min_value=0.01, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.01, step=1.0)
T = st.sidebar.number_input("Time to Expiry (years)", value=1.0, min_value=0.01, max_value=10.0, step=0.1)
r = st.sidebar.number_input("Risk-Free Rate", value=0.05, min_value=-0.05, max_value=0.30, step=0.005, format="%.3f")
vol = st.sidebar.number_input("Volatility (σ)", value=0.20, min_value=0.01, max_value=2.0, step=0.01, format="%.2f")
q = st.sidebar.number_input("Dividend Yield (q)", value=0.0, min_value=0.0, max_value=0.20, step=0.005, format="%.3f")
numsims = int(st.sidebar.number_input("Number of Simulations", value=1, min_value=1, max_value=1000000000000, step=1))
increment = st.sidebar.number_input("Increment as fraction of year", value=0.01, min_value=0.00000001, max_value=100000.0, step=0.0000001, format="%.3f")
dropdown = st.sidebar.selectbox("Asset process" ( "Arithmetic Brownian Motion", "Geometric  Brownian Motion"))

#simulate the process paths

process_model = mc.GBMmodel(r,q,vol,T,increment) #we create an object for the process model we want (possibly change this to something else using a dropdown int he future)
simulation = mc.monteCarlo(S,r,q,vol, T,increment,numsims, process_model)
simulation.run_sim()


fig = make_subplots(rows=1, cols=2,subplot_titles=("Simulated Paths (Visualisation limited to 2000 paths)", "Distribution of terminal spot price"),horizontal_spacing=0.1,)
if numsims >= 2000:
    for i in range(2000):
        fig.add_trace(go.Scatter(y=simulation.simulated_matrix[i,:], mode="lines",name=f"path {i}"), row=1, col=1)
else:
    for i in range(numsims):
        fig.add_trace(go.Scatter(y=simulation.simulated_matrix[i,:], mode="lines",name=f"path {i}"), row=1, col=1)
fig.add_trace(go.Histogram(y=simulation.simulated_matrix[:,-1],nbinsy=100),row=1,col=2)
    

st.plotly_chart(fig, use_container_width=True)

#price the greeks across the spot range and then plot them





