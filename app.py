"""
ScreenSense 3D - Coimbatore Multiplex Edition
---------------------------------------------
Features:
- Coimbatore Theatres Directory with Live Coordinates & Google Maps Pin
- In-App Cinema Seating & Ergonomic Booking Engine
- Dynamic Pricing with Visual Comfort Index (VCI)
- Instant Digital Boarding Pass with Verified QR Code
- 3D Virtual Auditorium Sightline Mesh
"""

import io
import os
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import qrcode
import streamlit as st

st.set_page_config(
    page_title="ScreenSense 3D | Coimbatore Cinemas",
    page_icon="🎬",
    layout="wide"
)

GEOMETRY_CSV = "theater_seats_geometry.csv"
MODEL_PKL = "pricing_model.pkl"

if not os.path.exists(GEOMETRY_CSV) or not os.path.exists(MODEL_PKL):
    st.error("Missing required artifacts! Run geometry_engine.py and train_model.py first.")
    st.stop()


@st.cache_data
def load_theater_geometry():
    return pd.read_csv(GEOMETRY_CSV)


@st.cache_resource
def load_trained_pipeline():
    with open(MODEL_PKL, "rb") as f:
        artifacts = pickle.load(f)
    return artifacts["model"], artifacts["feature_columns"]


seats_df = load_theater_geometry()
model, feature_columns = load_trained_pipeline()

# Coimbatore Theatres Database with Real Coordinates
COIMBATORE_THEATRES = {
    "KG Cinemas (Race Course)": {
        "lat": 11.0028,
        "lon": 76.9740,
        "address": "Bungalow Road, Race Course, Coimbatore",
        "screens": ["Screen 1 - 4K Laser Dolby Atmos", "Screen 2 - RGB Laser"],
        "screen_mult": 1.15
    },
    "INOX - Brookefields Mall (Krishnaswamy Rd)": {
        "lat": 11.0116,
        "lon": 76.9572,
        "address": "Brookefields Mall, Krishnaswamy Road, Coimbatore",
        "screens": ["Audi 1 - INSIGNIA VIP", "Audi 3 - Dolby Atmos"],
        "screen_mult": 1.25
    },
    "Broadway Cinemas - EPIQ (Avinashi Road)": {
        "lat": 11.0366,
        "lon": 77.0378,
        "address": "KMCH Opp, Avinashi Road, Civil Aerodrome, Coimbatore",
        "screens": ["EPIQ Giant Screen 1", "Gold Screen 2 (Laser 4K)"],
        "screen_mult": 1.35
    },
    "PVR INOX - Prozone Mall (Saravanampatti)": {
        "lat": 11.0558,
        "lon": 76.9942,
        "address": "Prozone Mall, Sathy Road, Saravanampatti, Coimbatore",
        "screens": ["Audi 2 - 4K Dolby 7.1", "Audi 5 - Large Screen"],
        "screen_mult": 1.20
    },
    "Ganga Yamuna Kaveri Complex (Gandhipuram)": {
        "lat": 11.0185,
        "lon": 76.9665,
        "address": "Cross Cut Road, Gandhipuram, Coimbatore",
        "screens": ["Ganga Screen (RGB 4K)", "Yamuna Screen"],
        "screen_mult": 1.05
    }
}

if "selected_seats" not in st.session_state:
    st.session_state.selected_seats = []

# --- Sidebar Portal Navigation ---
st.sidebar.title("🎦 ScreenSense 3D")
st.sidebar.caption("📍 Coimbatore Multiplex Network")

app_mode = st.sidebar.radio(
    "Choose View",
    ["🎟️ Book Tickets (Coimbatore Theatres)", "📊 3D Auditorium & Business Yield"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Select Theatre")

chosen_theatre_name = st.sidebar.selectbox(
    "Coimbatore Multiplexes:",
    list(COIMBATORE_THEATRES.keys())
)
theatre_info = COIMBATORE_THEATRES[chosen_theatre_name]

chosen_screen = st.sidebar.selectbox("Choose Audi / Screen:", theatre_info["screens"])
selected_genre = st.sidebar.selectbox("Film Genre:", ["Action", "Drama", "Horror", "Comedy", "Sci-Fi"])
selected_slot = st.sidebar.selectbox("Show Time:", ["Morning (10:30 AM)", "Matinee (02:00 PM)", "Evening (06:30 PM)", "Night (10:00 PM)"])
selected_day = st.sidebar.radio("Day:", ["Weekday", "Weekend"])
demand_surcharge = st.sidebar.slider("Dynamic Peak Multiplier:", 0.8, 1.5, 1.0, 0.05)

# Map show slot for ML model
model_slot = selected_slot.split()[0]

# --- ML Inference ---
inference_df = seats_df.copy()
inference_df["genre"] = selected_genre
inference_df["show_slot"] = model_slot
inference_df["day_type"] = selected_day

encoded_input = pd.get_dummies(
    inference_df[["pos_y", "vertical_tilt_deg", "fov_horizontal_deg", "yaw_deg", "vci_score", "genre", "show_slot", "day_type"]],
    drop_first=True
)

for col in feature_columns:
    if col not in encoded_input.columns:
        encoded_input[col] = 0
encoded_input = encoded_input[feature_columns]

predicted_prices = model.predict(encoded_input)
multiplier_combined = demand_surcharge * theatre_info["screen_mult"]
inference_df["predicted_price"] = np.round(predicted_prices * multiplier_combined, 0)


def assign_tier(vci):
    if vci >= 80:
        return "Prime Comfort (Sweet Spot)"
    elif vci >= 55:
        return "Standard Viewing"
    else:
        return "Ergonomic Discounted (Front Rows)"

inference_df["seat_tier"] = inference_df["vci_score"].apply(assign_tier)


def generate_qr(payload: str):
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#111111", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ==========================================
# VIEW 1: COIMBATORE CINEMAS BOOKING PORTAL
# ==========================================
if app_mode == "🎟️ Book Tickets (Coimbatore Theatres)":
    st.title(f"🎬 {chosen_theatre_name}")
    st.markdown(f"📍 **Address:** {theatre_info['address']} • **Selected Screen:** `{chosen_screen}`")

    # Theatre Map & Live Navigation Row
    with st.expander("🗺️ View Theatre on Map & Google Navigation", expanded=True):
        map_col1, map_col2 = st.columns([3, 1.2])

        with map_col1:
            map_data = pd.DataFrame([{"lat": theatre_info["lat"], "lon": theatre_info["lon"]}])
            st.map(map_data, zoom=14, height=220)

        with map_col2:
            st.markdown("#### 🧭 Live Navigation")
            gmaps_url = f"https://www.google.com/maps/search/?api=1&query={theatre_info['lat']},{theatre_info['lon']}"
            st.markdown(f"[![Open In Google Maps](https://img.shields.io/badge/Open_in-Google_Maps-4285F4?style=for-the-badge&logo=google-maps&logoColor=white)]({gmaps_url})")
            st.caption("Click button to get turn-by-turn driving directions from your location.")

    st.markdown("---")

    # Live Fare Strip
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Movie Format", f"{selected_genre}")
    with k2:
        st.metric("Show Schedule", f"{selected_slot.split()[0]} ({selected_day})")
    with k3:
        front_fare = int(inference_df[inference_df["row"] == "A"]["predicted_price"].mean())
        st.metric("Front Row Fair Fare", f"₹{front_fare}", delta="-35% Neck Comfort Relief")
    with k4:
        prime_fare = int(inference_df[inference_df["row"] == "F"]["predicted_price"].mean())
        st.metric("Sweet-Spot Fare", f"₹{prime_fare}", delta="+THX Calibrated")

    st.markdown("---")

    col_view, col_cart = st.columns([2.4, 1.4])

    with col_view:
        st.subheader("💺 Cinema Seating Floor Plan")
        st.caption("Screen is on top. Front rows (A–B) are dynamically discounted for neck comfort.")

        fig_2d = px.scatter(
            inference_df,
            x="col",
            y="row",
            color="seat_tier",
            size="vci_score",
            hover_name="seat_id",
            hover_data={
                "predicted_price": ":.0f",
                "vci_score": ":.1f",
                "vertical_tilt_deg": ":.1f",
                "col": False,
                "row": False,
                "seat_tier": True
            },
            color_discrete_map={
                "Prime Comfort (Sweet Spot)": "#00CC96",
                "Standard Viewing": "#FFA15A",
                "Ergonomic Discounted (Front Rows)": "#EF553B"
            }
        )
        fig_2d.update_yaxes(autorange="reversed", title="Row (A = Screen Front)")
        fig_2d.update_xaxes(title="Seat Column", tickmode="linear", dtick=1)
        fig_2d.update_layout(
            height=460,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_2d, width="stretch")

    with col_cart:
        st.subheader("🛒 In-App Ticket Checkout")

        all_seat_list = inference_df["seat_id"].tolist()
        user_picks = st.multiselect(
            "Select Seats to Book:",
            options=all_seat_list,
            default=st.session_state.selected_seats,
            placeholder="Choose seats (e.g. A3, F5, F6)..."
        )
        st.session_state.selected_seats = user_picks

        if user_picks:
            selected_records = inference_df[inference_df["seat_id"].isin(user_picks)]
            total_fare = 0.0

            for _, seat in selected_records.iterrows():
                fare = seat["predicted_price"]
                vci = seat["vci_score"]
                tilt = seat["vertical_tilt_deg"]
                total_fare += fare

                with st.container():
                    st.markdown(f"**Seat {seat['seat_id']}** • ₹{int(fare)}")
                    if vci < 60:
                        st.warning(f"⚠️ {tilt:.1f}° Neck Tilt | Comfort: {vci:.0f}/100", icon="⚠️")
                    else:
                        st.success(f"✨ {tilt:.1f}° Sightline | Comfort: {vci:.0f}/100", icon="✨")
                    st.divider()

            convenience_fee = len(user_picks) * 25.0
            grand_total = total_fare + convenience_fee

            st.write(f"**Base Fares:** ₹{int(total_fare):,}")
            st.write(f"**Convenience Fee:** ₹{int(convenience_fee):,}")
            st.markdown(f"### **Total Amount: ₹{int(grand_total):,}**")

            if st.button("💳 Confirm Booking & Generate Boarding Pass", type="primary", use_container_width=True):
                st.session_state.booked_confirmed = True
                st.balloons()
        else:
            st.info("Pick seats from the floor plan to calculate real-time fares.")

    # Live Digital Boarding Pass
    if st.session_state.get("booked_confirmed", False) and user_picks:
        st.markdown("---")
        st.subheader("🎟️ Confirmed Digital Cinema Pass")

        p_col1, p_col2 = st.columns([2, 1])
        with p_col1:
            st.markdown(f"""
            ### **{chosen_theatre_name}**
            * **Auditorium:** {chosen_screen}
            * **Show Details:** {selected_genre} Presentation • {selected_slot}
            * **Seats Booked:** **{', '.join(user_picks)}**
            * **Total Paid:** **₹{int(grand_total):,}** (Dynamic Ergonomics Calibrated)
            * **Location:** {theatre_info['address']}
            """)
            st.caption("✅ Confirmed via ScreenSense 3D. Show this QR at the turnstile gate.")

        with p_col2:
            ticket_payload = (
                f"SCREENSENSE-CBE-PASS|THEATRE={chosen_theatre_name}|AUDI={chosen_screen}|"
                f"SEATS={','.join(user_picks)}|TOTAL=INR_{int(grand_total)}|MAP={theatre_info['lat']},{theatre_info['lon']}"
            )
            qr_bytes = generate_qr(ticket_payload)
            st.image(qr_bytes, caption="Turnstile Scan QR", width=180)
            st.download_button(
                label="📥 Download Ticket Pass",
                data=qr_bytes,
                file_name=f"screensense_ticket_{user_picks[0]}.png",
                mime="image/png"
            )


# ==========================================
# VIEW 2: 3D AUDITORIUM & BUSINESS YIELD
# ==========================================
else:
    st.title("📊 Multiplex Executive Telemetry & 3D Optics")
    st.caption(f"Spatial analytics and dead-zone yield recovery for {chosen_theatre_name}.")

    tab1, tab2 = st.tabs(["🏛️ 3D Virtual Auditorium Mesh", "📈 Commercial Dead-Zone Recovery"])

    with tab1:
        st.subheader("Auditorium Spatial Elevation Model")
        fig_3d = go.Figure()

        fig_3d.add_trace(go.Scatter3d(
            x=inference_df["col"],
            y=inference_df["pos_y"],
            z=inference_df["vertical_tilt_deg"],
            mode="markers",
            marker=dict(
                size=6,
                color=inference_df["vci_score"],
                colorscale="Viridis",
                colorbar=dict(title="VCI"),
                opacity=0.9
            ),
            text=[f"Seat: {sid}<br>Row: {r}<br>Tilt: {t:.1f}°<br>Price: ₹{p:.0f}"
                  for sid, r, t, p in zip(inference_df["seat_id"], inference_df["row"], inference_df["vertical_tilt_deg"], inference_df["predicted_price"])],
            hoverinfo="text",
            name="Seating Grid"
        ))

        # Cinema Screen Wall in 3D
        screen_x = [1, 14, 14, 1, 1]
        screen_y = [0, 0, 0, 0, 0]
        screen_z = [0, 0, 45, 45, 0]

        fig_3d.add_trace(go.Scatter3d(
            x=screen_x, y=screen_y, z=screen_z,
            mode="lines",
            line=dict(color="#FF4B4B", width=9),
            name="Display Screen"
        ))

        fig_3d.update_layout(
            scene=dict(
                xaxis_title="Seat Column",
                yaxis_title="Distance from Screen (m)",
                zaxis_title="Neck Tilt (°)",
                camera=dict(eye=dict(x=-1.5, y=-1.8, z=1.2))
            ),
            height=580,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_3d, width="stretch")

    with tab2:
        st.subheader("Row-Wise Pricing Recovery")
        row_report = inference_df.groupby("row").agg(
            Average_Comfort=("vci_score", "mean"),
            Dynamic_Price=("predicted_price", "mean")
        ).reset_index()

        fig_bar = px.bar(
            row_report,
            x="row",
            y="Dynamic_Price",
            color="Average_Comfort",
            color_continuous_scale="RdYlGn",
            labels={"row": "Row (A = Front)", "Dynamic_Price": "Optimized Fare (₹)", "Average_Comfort": "Comfort Index"},
            title=f"Optimized Fare Distribution - {chosen_theatre_name}"
        )
        st.plotly_chart(fig_bar, width="stretch")