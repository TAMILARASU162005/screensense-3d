"""
ScreenSense 3D - Interactive Streamlit Dashboard
------------------------------------------------
Visualizes theater seating geometry, Visual Comfort Index (VCI),
and predicts real-time dynamic pricing using the trained LightGBM model.
"""

import os
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure page layout
st.set_page_config(
    page_title="ScreenSense 3D | Dynamic Cinema Pricing",
    page_icon="🎬",
    layout="wide"
)

# Custom header styling
st.title("🎬 ScreenSense 3D: Ergonomic Seating & Dynamic Pricing")
st.markdown(
    "Trigonometric field-of-view (FOV) and vertical neck strain analytics "
    "powering fair dynamic ticket pricing."
)

GEOMETRY_CSV = "theater_seats_geometry.csv"
MODEL_PKL = "pricing_model.pkl"

# Verify prerequisite artifacts
if not os.path.exists(GEOMETRY_CSV) or not os.path.exists(MODEL_PKL):
    st.error(
        "Missing required artifacts! Please run `geometry_engine.py` and "
        "`train_model.py` first to generate geometry data and trained model."
    )
    st.stop()


@st.cache_data
def load_theater_geometry():
    return pd.read_csv(GEOMETRY_CSV)


@st.cache_resource
def load_trained_pipeline():
    with open(MODEL_PKL, "rb") as f:
        artifacts = pickle.load(f)
    return artifacts["model"]


seats_df = load_theater_geometry()
model = load_trained_pipeline()

# --- Sidebar Parameter Controls ---
st.sidebar.header("🕹️ Show Parameters")

selected_genre = st.sidebar.selectbox(
    "Movie Genre",
    ["Action", "Drama", "Horror", "Comedy", "Sci-Fi"]
)

selected_slot = st.sidebar.selectbox(
    "Show Slot",
    ["Morning", "Matinee", "Evening", "Night"]
)

selected_day = st.sidebar.radio(
    "Day of the Week",
    ["Weekday", "Weekend"]
)

base_inflation = st.sidebar.slider(
    "Demand Surcharge Multiplier",
    min_value=0.8,
    max_value=1.5,
    value=1.0,
    step=0.05
)

# --- Feature Preparation for Prediction ---
inference_df = seats_df.copy()
inference_df["genre"] = selected_genre
inference_df["show_slot"] = selected_slot
inference_df["day_type"] = selected_day

# Ensure categorical typing matches model training
for col in ["genre", "show_slot", "day_type"]:
    inference_df[col] = inference_df[col].astype("category")

features = [
    "pos_y",
    "vertical_tilt_deg",
    "fov_horizontal_deg",
    "yaw_deg",
    "vci_score",
    "genre",
    "show_slot",
    "day_type"
]

predicted_prices = model.predict(inference_df[features])
inference_df["predicted_price"] = np.round(predicted_prices * base_inflation, 0)

# --- Metric KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_price = int(inference_df["predicted_price"].mean())
    st.metric("Average Ticket Price", f"₹{avg_price}")

with col2:
    front_discount = int(inference_df[inference_df["row"] == "A"]["predicted_price"].mean())
    st.metric("Front Row Discounted Price", f"₹{front_discount}")

with col3:
    prime_price = int(inference_df[inference_df["row"] == "F"]["predicted_price"].mean())
    st.metric("Prime Row (Sweet Spot) Price", f"₹{prime_price}")

with col4:
    avg_vci = round(inference_df["vci_score"].mean(), 1)
    st.metric("Overall Theater Comfort Score", f"{avg_vci} / 100")

st.markdown("---")

# --- Interactive Visualizations ---
tab1, tab2 = st.tabs(["💺 Dynamic Seating Heatmap", "📊 Visual Comfort vs Price Analysis"])

with tab1:
    st.subheader("Interactive Screen & Seating Layout")
    st.caption("Hover over any seat to inspect ergonomic angles and recommended fares.")

    # Render Screen indicator
    screen_indicator = go.Figure()
    
    fig = px.scatter(
        inference_df,
        x="col",
        y="row",
        color="predicted_price",
        size="vci_score",
        color_continuous_scale="Viridis",
        hover_data={
            "seat_id": True,
            "vci_score": True,
            "predicted_price": ":.0f",
            "vertical_tilt_deg": ":.1f",
            "fov_horizontal_deg": ":.1f",
            "row": False,
            "col": False
        },
        labels={
            "col": "Seat Column",
            "row": "Row (A=Front)",
            "predicted_price": "Price (₹)",
            "vci_score": "Comfort Score"
        }
    )

    # Invert Y axis so Row A stays nearest to the screen
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(tickmode="linear", tick0=1, dtick=1),
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Ergonomic Strain vs Dynamic Price Correlation")
    
    scatter_fig = px.scatter(
        inference_df,
        x="vertical_tilt_deg",
        y="predicted_price",
        color="vci_score",
        size="fov_horizontal_deg",
        color_continuous_scale="Thermal",
        labels={
            "vertical_tilt_deg": "Vertical Neck Tilt (Degrees)",
            "predicted_price": "Recommended Price (₹)",
            "vci_score": "Comfort Score"
        },
        hover_name="seat_id"
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

# --- Seat Data Table View ---
with st.expander("🔍 View Raw Seat Ergonomics & Pricing Data"):
    st.dataframe(
        inference_df[[
            "seat_id", "row", "col", "vci_score",
            "vertical_tilt_deg", "fov_horizontal_deg", "yaw_deg",
            "predicted_price"
        ]],
        use_container_width=True
    )