"""
ScreenSense 3D - Luxury Coimbatore Cinema Booking Hub
------------------------------------------------------
Features:
- Fixed stateful Booking confirmation & instant Turnstile QR Pass
- Clean, aligned Luxury Obsidian & Champagne Gold Cinema UI
- Direct 3D WebGL Cinema Canvas with Interactive Controls
- Coimbatore Multiplex Directory with live Google Maps routes
"""

import io
import os
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import qrcode
import streamlit as st
import streamlit.components.v1 as components

# --- 1. Page Configuration & Custom Luxury Styling ---
st.set_page_config(
    page_title="ScreenSense 3D | Luxury Cinema Hub",
    page_icon="🎬",
    layout="wide"
)

# Custom High-End Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background-color: #080A10;
        color: #E2E8F0;
    }
    
    /* Header Card */
    .cinema-header-card {
        background: linear-gradient(135deg, rgba(20, 24, 38, 0.85) 0%, rgba(10, 12, 18, 0.95) 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    .cinema-title {
        font-family: 'Cinzel', serif;
        color: #F8F5E9;
        font-size: 26px;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .cinema-subtitle {
        color: #D4AF37;
        font-size: 13px;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Metrics Pill */
    div[data-testid="stMetric"] {
        background: rgba(18, 22, 34, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 12px 16px;
    }
    
    /* Elegant Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #D4AF37 0%, #AA820A 100%);
        color: #0B0E14;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
        color: #000;
    }
    
    /* Ticket Box */
    .ticket-pass-box {
        background: radial-gradient(circle at 10% 10%, rgba(30, 35, 55, 0.9) 0%, rgba(14, 17, 26, 0.95) 100%);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 14px;
        padding: 22px;
        margin-top: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Load Assets & ML Models ---
GEOMETRY_CSV = "theater_seats_geometry.csv"
MODEL_PKL = "pricing_model.pkl"

if not os.path.exists(GEOMETRY_CSV) or not os.path.exists(MODEL_PKL):
    st.error("Model artifacts missing! Please verify geometry_engine.py & train_model.py have been executed.")
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

# Coimbatore Multiplex Data
COIMBATORE_THEATRES = {
    "Broadway Cinemas - EPIQ (Avinashi Road)": {
        "lat": 11.0366,
        "lon": 77.0378,
        "address": "KMCH Opp, Avinashi Road, Civil Aerodrome, Coimbatore",
        "screens": ["EPIQ Giant Screen 1 (Laser 4K)", "Gold Screen 2 (Dolby Atmos)"],
        "screen_mult": 1.35
    },
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
    "PVR INOX - Prozone Mall (Saravanampatti)": {
        "lat": 11.0558,
        "lon": 76.9942,
        "address": "Prozone Mall, Sathy Road, Saravanampatti, Coimbatore",
        "screens": ["Audi 2 - 4K Dolby 7.1", "Audi 5 - Large Format"],
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

# --- 3. Initialize Persistent Session States ---
if "booked_active" not in st.session_state:
    st.session_state.booked_active = False
if "confirmed_seats" not in st.session_state:
    st.session_state.confirmed_seats = []
if "confirmed_fare" not in st.session_state:
    st.session_state.confirmed_fare = 0

# --- 4. Sidebar Configuration Drawer ---
st.sidebar.markdown("### 🎬 Screenseense 3D Controls")

chosen_theatre_name = st.sidebar.selectbox("Multiplex Destination", list(COIMBATORE_THEATRES.keys()))
theatre_info = COIMBATORE_THEATRES[chosen_theatre_name]

chosen_screen = st.sidebar.selectbox("Auditorium / Screen", theatre_info["screens"])
selected_genre = st.sidebar.selectbox("Film Genre", ["Action", "Drama", "Horror", "Comedy", "Sci-Fi"])
selected_slot = st.sidebar.selectbox("Show Schedule", ["Morning (10:30 AM)", "Matinee (02:00 PM)", "Evening (06:30 PM)", "Night (10:00 PM)"])
selected_day = st.sidebar.radio("Day Type", ["Weekday", "Weekend"], horizontal=True)
demand_surcharge = st.sidebar.slider("Dynamic Peak Multiplier", 0.8, 1.5, 1.0, 0.05)

st.sidebar.markdown("---")
show_analytics = st.sidebar.checkbox("Executive Analytics Overlay", value=False)

# Inference Model Calculation
model_slot = selected_slot.split()[0]
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
    img = qr.make_image(fill_color="#0F172A", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# --- 5. Main Hero Banner & Information Strip ---
st.markdown(f"""
<div class="cinema-header-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="cinema-title">{chosen_theatre_name}</h1>
            <div class="cinema-subtitle">📍 {theatre_info['address']} &nbsp;|&nbsp; 📽️ {chosen_screen}</div>
        </div>
        <div style="margin-top: 8px;">
            <a href="https://www.google.com/maps/search/?api=1&query={theatre_info['lat']},{theatre_info['lon']}" target="_blank" style="text-decoration:none;">
                <button style="background: rgba(212,175,55,0.15); border: 1px solid #D4AF37; color:#F5D77F; padding: 7px 15px; border-radius: 6px; font-weight:600; cursor:pointer;">
                    📍 Open Google Maps Route
                </button>
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Telemetry Metrics
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Experience Format", selected_genre)
with k2:
    st.metric("Show Schedule", f"{selected_slot.split()[0]} ({selected_day})")
with k3:
    front_fare = int(inference_df[inference_df["row"] == "A"]["predicted_price"].mean())
    st.metric("Front Row Fair Fare", f"₹{front_fare}", delta="-35% Ergonomic Relief")
with k4:
    prime_fare = int(inference_df[inference_df["row"] == "F"]["predicted_price"].mean())
    st.metric("Sweet-Spot Fare", f"₹{prime_fare}", delta="+THX Calibrated")

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# --- 6. Direct Embedded 3D Canvas ---
st.markdown("### 🏛️ Interactive 3D Cinema Spatial Experience")
st.caption("Inspect stage riser slope, screen curvature and sightlines with mouse drag & zoom controls.")

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=720, scrolling=True)
else:
    st.info("💡 `index.html` not found in root directory.")

st.markdown("---")

# --- 7. Aligned Seating Layout & Persistent Booking Drawer ---
grid_col, invoice_col = st.columns([2.2, 1.4], gap="medium")

with grid_col:
    st.markdown("### 💺 Cinema Seating Floor Plan")
    st.caption("Top is Screen. Rows A-B are dynamically discounted for neck tilt.")

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
    fig_2d.update_yaxes(autorange="reversed", title="")
    fig_2d.update_xaxes(title="Column Number", tickmode="linear", dtick=1)
    fig_2d.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_2d, width="stretch")

with invoice_col:
    st.markdown("### 🛒 In-App Reservation")

    all_seats = inference_df["seat_id"].tolist()
    user_picks = st.multiselect(
        "Choose Seats:",
        options=all_seats,
        default=st.session_state.confirmed_seats if st.session_state.booked_active else [],
        placeholder="Select seat IDs (e.g., A4, F6)..."
    )

    if user_picks:
        selected_records = inference_df[inference_df["seat_id"].isin(user_picks)]
        subtotal = float(selected_records["predicted_price"].sum())
        convenience = float(len(user_picks) * 25.0)
        total_fare = subtotal + convenience

        for _, seat in selected_records.iterrows():
            st.markdown(f"**Seat {seat['seat_id']}** • ₹{int(seat['predicted_price'])} &nbsp;|&nbsp; Comfort: **{seat['vci_score']:.0f}/100**")

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-radius: 8px; padding: 12px; margin-top: 10px;">
            <div style="display:flex; justify-content:space-between;"><span>Ticket Base:</span><span>₹{int(subtotal):,}</span></div>
            <div style="display:flex; justify-content:space-between;"><span>Booking Fee:</span><span>₹{int(convenience):,}</span></div>
            <hr style="margin: 8px 0; border-color: rgba(255,255,255,0.1);">
            <div style="display:flex; justify-content:space-between; font-size: 18px; font-weight:700; color:#D4AF37;">
                <span>Total Amount:</span><span>₹{int(total_fare):,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # Action Button Triggering State Lock
        if st.button("💳 Confirm & Generate Boarding Pass", key="btn_confirm_booking", use_container_width=True):
            st.session_state.booked_active = True
            st.session_state.confirmed_seats = user_picks
            st.session_state.confirmed_fare = total_fare
            st.rerun()

    else:
        st.session_state.booked_active = False
        st.info("Pick seats from the grid to view dynamic fares and confirm booking.")

# --- 8. Persistent Verified QR Boarding Pass ---
if st.session_state.booked_active and st.session_state.confirmed_seats:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.balloons()
    
    st.markdown("### 🎟️ Official Turnstile Boarding Pass")

    pass_col1, pass_col2 = st.columns([2.3, 1.2])

    with pass_col1:
        st.markdown(f"""
        <div class="ticket-pass-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="font-family:'Cinzel', serif; margin:0; color:#F5D77F;">{chosen_theatre_name}</h2>
                <span style="background:rgba(0,204,150,0.2); color:#00CC96; padding: 4px 10px; border-radius: 6px; font-weight:700; font-size:12px;">CONFIRMED</span>
            </div>
            <div style="margin: 12px 0; color:#94A3B8; font-size:14px;">
                Auditorium: <strong style="color:#FFF;">{chosen_screen}</strong> &nbsp;•&nbsp; 
                Format: <strong style="color:#FFF;">{selected_genre}</strong> &nbsp;•&nbsp; 
                Time: <strong style="color:#FFF;">{selected_slot}</strong>
            </div>
            <div style="font-size: 20px; font-weight: 700; color: #FFF; margin: 10px 0;">
                Confirmed Seats: <span style="color:#D4AF37;">{', '.join(st.session_state.confirmed_seats)}</span>
            </div>
            <div style="color: #94A3B8; font-size: 13px;">
                Total Billed: <strong style="color:#FFF;">₹{int(st.session_state.confirmed_fare):,}</strong> (Dynamic SMPTE Ergonomic Pricing Calibrated)
            </div>
            <div style="margin-top: 15px; font-size: 12px; color: #64748B;">
                📍 {theatre_info['address']}<br>
                Please present the digital QR code at the turnstile gate for verified entry.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with pass_col2:
        qr_string = (
            f"SCREENSENSE-CBE-PASS|THEATRE={chosen_theatre_name}|AUDI={chosen_screen}|"
            f"SEATS={','.join(st.session_state.confirmed_seats)}|TOTAL=INR_{int(st.session_state.confirmed_fare)}|"
            f"MAP_LATLON={theatre_info['lat']},{theatre_info['lon']}"
        )
        qr_image_bytes = generate_qr(qr_string)
        
        st.markdown("<div style='text-align:center; padding-top: 10px;'>", unsafe_allow_html=True)
        st.image(qr_image_bytes, caption="Turnstile QR Verification", width=180)
        st.download_button(
            label="📥 Download Pass PNG",
            data=qr_image_bytes,
            file_name=f"screensense_boarding_pass_{st.session_state.confirmed_seats[0]}.png",
            mime="image/png",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

# --- 9. Executive Yield Analytics (Optional Drawer) ---
if show_analytics:
    st.markdown("---")
    st.subheader("📈 Executive Dead-Zone Recovery Breakdown")
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
        title=f"Optimized Fare Distribution Across Rows - {chosen_theatre_name}"
    )
    st.plotly_chart(fig_bar, width="stretch")