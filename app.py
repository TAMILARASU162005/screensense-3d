"""
ScreenSense 3D | Triple-Portal Cinema OS & Analytics Platform
=============================================================
1. Audience Portal: 3D Seating, Atmos Audio Spectrum, F&B Delivery & Checkout
2. Executive Analytics Portal: Real-time SPH, Heatmaps & Yield Simulator
3. Turnstile Security Scanner: Entry Gate Staff Biometric Verification
"""

import io
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import qrcode
import streamlit as st

st.set_page_config(
    page_title="ScreenSense 3D | Cinema OS",
    page_icon="🎬",
    layout="wide"
)

# Custom High-Voltage Cyber-Cinema Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0B1528 0%, #030712 70%, #010307 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F1F5F9;
    }

    #MainMenu, header, footer {visibility: hidden;}

    .master-ribbon {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(3, 7, 18, 0.98) 100%);
        border: 1px solid rgba(6, 182, 212, 0.45);
        border-radius: 16px;
        padding: 16px 26px;
        margin-bottom: 20px;
        box-shadow: 0 0 35px rgba(6, 182, 212, 0.15), 0 20px 40px rgba(0, 0, 0, 0.85);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #06B6D4 50%, #FACC15 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: 1.5px;
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
    }

    .kpi-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.12);
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #10B981;
    }
    .kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #94A3B8;
        letter-spacing: 0.9px;
    }

    .gateway-box {
        background: rgba(11, 18, 32, 0.95);
        border: 1px solid rgba(250, 204, 21, 0.4);
        border-radius: 14px;
        padding: 22px;
        backdrop-filter: blur(16px);
        box-shadow: 0 0 30px rgba(250, 204, 21, 0.1);
    }
    .invoice-line {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        margin-bottom: 8px;
        color: #94A3B8;
    }
    .invoice-line strong { color: #F8FAFC; }
    .invoice-total-line {
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        margin-top: 12px;
        padding-top: 10px;
        display: flex;
        justify-content: space-between;
        font-size: 22px;
        font-weight: 800;
        color: #FACC15;
        font-family: 'Space Grotesk', sans-serif;
    }

    .boarding-pass-wrap {
        background: radial-gradient(circle at 10% 10%, #0F172A 0%, #020617 100%);
        border: 1px solid rgba(6, 182, 212, 0.6);
        border-radius: 18px;
        padding: 26px;
        margin-top: 25px;
        box-shadow: 0 0 40px rgba(6, 182, 212, 0.2), 0 25px 60px rgba(0, 0, 0, 0.95);
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FACC15 0%, #F59E0B 100%) !important;
        color: #030712 !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 13px 24px !important;
        letter-spacing: 0.9px !important;
        text-transform: uppercase !important;
        box-shadow: 0 6px 25px rgba(250, 204, 21, 0.35) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 35px rgba(250, 204, 21, 0.55) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DIRECTORY & GROUND-TRUTH PRICING
# ---------------------------------------------------------
COIMBATORE_THEATRES = {
    "Broadway Cinemas - EPIQ (Avinashi Rd)": {
        "addr": "Avinashi Road, Civil Aerodrome, Coimbatore",
        "screens": ["EPIQ Giant Screen 1 (4K Laser)", "Gold Screen 2 (Dolby Atmos)"],
        "lat": 11.0366, "lon": 77.0378,
        "pricing": {"front": 130, "standard": 210, "prime": 290},
        "sound": "Barco 4K Laser + Meyer Sound 64-Ch Atmos"
    },
    "KG Cinemas (Race Course)": {
        "addr": "Bungalow Road, Race Course, Coimbatore",
        "screens": ["Screen 1 - 4K Laser Dolby Atmos", "Screen 2 - RGB Laser 7.1"],
        "lat": 11.0028, "lon": 76.9740,
        "pricing": {"front": 90, "standard": 150, "prime": 210},
        "sound": "Dolby Atmos Spatial Cinema Audio"
    },
    "INOX - Brookefields Mall (Krishnaswamy Rd)": {
        "addr": "Brookefields Mall, Krishnaswamy Road, Coimbatore",
        "screens": ["Audi 1 - INSIGNIA VIP Lux", "Audi 3 - Club Atmos"],
        "lat": 11.0116, "lon": 76.9572,
        "pricing": {"front": 120, "standard": 190, "prime": 280},
        "sound": "INSIGNIA Plush Dolby Atmos"
    },
    "PVR INOX - Prozone Mall (Saravanampatti)": {
        "addr": "Prozone Mall, Sathy Road, Saravanampatti, Coimbatore",
        "screens": ["Audi 2 - 4K Dolby Atmos", "Audi 5 - Large Format Screen"],
        "lat": 11.0558, "lon": 76.9942,
        "pricing": {"front": 110, "standard": 180, "prime": 260},
        "sound": "Christie 4K Laser + Dolby 7.1 Array"
    },
    "Ganga Yamuna Kaveri Complex (Gandhipuram)": {
        "addr": "Cross Cut Road, Gandhipuram, Coimbatore",
        "screens": ["Ganga Screen (RGB 4K Laser)", "Yamuna Screen (Dolby Atmos)"],
        "lat": 11.0185, "lon": 76.9665,
        "pricing": {"front": 80, "standard": 120, "prime": 160},
        "sound": "Linear Acoustic Baffles Dual Laser"
    }
}

# ---------------------------------------------------------
# SPATIAL AUDITORIUM GEOMETRY & ACOUSTIC SIMULATION
# ---------------------------------------------------------
@st.cache_data
def load_multiplex_dataset():
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = 12
    records = []

    for r_idx, r in enumerate(rows):
        dist_y = 3.6 + (r_idx * 2.5)
        elev_z = r_idx * 0.95
        tilt = np.degrees(np.arctan((6.8 - elev_z) / dist_y))

        for c in range(1, cols + 1):
            x_off = (c - (cols / 2 + 0.5)) * 1.5
            yaw = np.degrees(np.arctan(x_off / dist_y))
            vci = max(25, min(99, 100 - (abs(tilt - 13.5) * 2.3 + abs(yaw) * 1.6)))

            screen_span = 24.0
            fov_deg = np.degrees(2 * np.arctan((screen_span / 2) / dist_y))

            dist_center = np.sqrt(x_off**2 + (dist_y - 12.0)**2)
            audio_immersion = max(55, min(99, 100 - (dist_center * 2.8)))
            spl_db = round(85.0 - (dist_y * 0.45) + (elev_z * 0.3), 1)

            if r in ['A', 'B']:
                tier = "Ergonomic Discount (Front)"
                tier_key = "front"
                base_color = "#F43F5E"
                fill_rate = 32.5
            elif r in ['E', 'F', 'G']:
                tier = "Prime Sweet Spot (THX VIP)"
                tier_key = "prime"
                base_color = "#10B981"
                fill_rate = 94.0
            else:
                tier = "Standard Eye-Level"
                tier_key = "standard"
                base_color = "#06B6D4"
                fill_rate = 74.5

            records.append({
                "seat_id": f"{r}{c}",
                "row": r,
                "col": c,
                "x": x_off,
                "y": dist_y,
                "z": elev_z,
                "tilt": tilt,
                "vci": vci,
                "fov_deg": round(fov_deg, 1),
                "audio_immersion": audio_immersion,
                "spl_db": spl_db,
                "tier": tier,
                "tier_key": tier_key,
                "base_color": base_color,
                "historical_fill_rate": fill_rate
            })

    return pd.DataFrame(records)

seats_df = load_multiplex_dataset()
all_seat_ids = seats_df["seat_id"].tolist()

# ---------------------------------------------------------
# STATE INITIALIZATION
# ---------------------------------------------------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "selected_portal" not in st.session_state:
    st.session_state.selected_portal = "🎟️ Audience Booking Portal"
if "selected_seats" not in st.session_state:
    st.session_state.selected_seats = ["E5", "E6"]
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "txn_receipt" not in st.session_state:
    st.session_state.txn_receipt = None
if "admin_dynamic_surge" not in st.session_state:
    st.session_state.admin_dynamic_surge = 1.05
if "global_theatre_name" not in st.session_state:
    st.session_state.global_theatre_name = "Broadway Cinemas - EPIQ (Avinashi Rd)"

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & CLIMATE ENGINE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎦 Multiplex Navigator")
    sel_theatre_name = st.selectbox(
        "Select Cinema:",
        list(COIMBATORE_THEATRES.keys()),
        index=list(COIMBATORE_THEATRES.keys()).index(st.session_state.global_theatre_name)
    )
    st.session_state.global_theatre_name = sel_theatre_name
    t_meta = COIMBATORE_THEATRES[sel_theatre_name]
    sel_audi = st.selectbox("Auditorium:", t_meta["screens"])

    st.markdown("---")
    genre = st.radio("Presentation Format:", ["Action (Laser 4K)", "Sci-Fi (Dolby Atmos)", "Drama (IMAX)"], index=0)
    slot = st.selectbox("Show Time:", ["10:30 AM", "02:15 PM", "06:45 PM", "10:15 PM"], index=2)
    day = st.radio("Day Type:", ["Weekday", "Weekend / Holiday"], horizontal=True)

    st.markdown("---")
    st.markdown("### 🌦️ Coimbatore Weather Engine")
    weather_cond = st.selectbox(
        "Climate Conditions:",
        ["Sunny / Clear Evening (Normal Footfall)", "Heavy Monsoon Rain (+12% Rush)", "Festival Long Weekend (+25% Surge)"]
    )
    weather_multiplier = 1.25 if "Festival" in weather_cond else 1.12 if "Rain" in weather_cond else 1.0

# Dynamic Global Price Sync
effective_surge = float(st.session_state.admin_dynamic_surge) * weather_multiplier
t_pricing = t_meta["pricing"]
seats_df["fare"] = seats_df["tier_key"].map(lambda k: round(t_pricing[k] * effective_surge, 0))

# ---------------------------------------------------------
# TOP PORTAL SWITCHER RIBBON (3 PORTALS)
# ---------------------------------------------------------
ribbon_left, ribbon_right = st.columns([2.2, 1.8])
with ribbon_left:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:32px;">🎬</span>
        <div>
            <h1 class="brand-title">SCREENSENSE 3D</h1>
            <div style="font-size:11px; color:#94A3B8; letter-spacing:1.5px; font-weight:600;">COIMBATORE CINEMA OPERATING SYSTEM & BI SUITE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with ribbon_right:
    portal_choice = st.radio(
        "Platform Gateways:",
        ["🎟️ Audience Booking Portal", "🏢 Theatre Manager Admin (BI)", "🛡️ Turnstile Gate Scanner"],
        horizontal=True,
        index=["🎟️ Audience Booking Portal", "🏢 Theatre Manager Admin (BI)", "🛡️ Turnstile Gate Scanner"].index(st.session_state.selected_portal)
    )
    st.session_state.selected_portal = portal_choice

st.markdown("---")

# =========================================================
# PORTAL 1: AUDIENCE / CUSTOMER VIEW
# =========================================================
if st.session_state.selected_portal == "🎟️ Audience Booking Portal":

    st.markdown(f"""
    <div class="master-ribbon">
        <div>
            <h2 style="font-family:'Cinzel', serif; font-size:22px; color:#FFF; margin:0;">{sel_theatre_name.split(' - ')[0]}</h2>
            <p style="color:#94A3B8; font-size:12px; margin:3px 0 0 0;">📍 {t_meta['addr']} &nbsp;•&nbsp; 📽️ {sel_audi}</p>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:12px; color:#06B6D4; background:rgba(6,182,212,0.12); padding:6px 14px; border-radius:12px; border:1px solid rgba(6,182,212,0.35); font-weight:700;">
                🌦️ Footfall Factor: {weather_multiplier:.2f}x
            </span>
            <a href="https://www.google.com/maps/search/?api=1&query={t_meta['lat']},{t_meta['lon']}" target="_blank" style="text-decoration:none;">
                <button style="background:rgba(250,204,21,0.15); border:1px solid #FACC15; color:#FACC15; padding:8px 16px; border-radius:8px; font-weight:800; cursor:pointer; font-size:12px;">
                    🧭 Live Maps
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def render_customer_3d(df, selected_ids):
        fig = go.Figure()

        scr_x = np.linspace(-12, 12, 40)
        scr_z = np.linspace(1.8, 9.2, 20)
        X, Z = np.meshgrid(scr_x, scr_z)
        Y = -0.025 * (X**2)

        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale=[[0, '#06B6D4'], [0.3, '#10B981'], [0.5, '#FFFFFF'], [0.7, '#10B981'], [1, '#06B6D4']],
            showscale=False, name="Silver Screen", hoverinfo="name"
        ))

        for r_idx in range(len(df['row'].unique())):
            y_start = 3.2 + (r_idx * 2.5)
            z_height = r_idx * 0.95
            fig.add_trace(go.Mesh3d(
                x=[-11, 11, 11, -11, -11, 11, 11, -11],
                y=[y_start, y_start, y_start + 2.3, y_start + 2.3, y_start, y_start, y_start + 2.3, y_start + 2.3],
                z=[0, 0, 0, 0, z_height, z_height, z_height, z_height],
                color="#0A1120", opacity=0.85, hoverinfo="skip"
            ))

        for sel_id in selected_ids:
            s_row = df[df["seat_id"] == sel_id]
            if not s_row.empty:
                s = s_row.iloc[0]
                fig.add_trace(go.Scatter3d(
                    x=[s["x"], 0], y=[s["y"], 0], z=[s["z"] + 0.5, 5.5],
                    mode="lines", line=dict(color="#FACC15", width=6, dash="solid"), hoverinfo="skip"
                ))

        colors, sizes, symbols, hover_texts = [], [], [], []
        for _, s in df.iterrows():
            is_sel = s["seat_id"] in selected_ids
            c = "#FACC15" if is_sel else s["base_color"]
            sz = 14 if is_sel else 9
            badge = "⭐ [SELECTED]" if is_sel else "🟢 [INSPECT & BOOK]"

            colors.append(c)
            sizes.append(sz)
            symbols.append("circle")
            hover_texts.append(
                f"<b>Seat: {s['seat_id']}</b> | {badge}<br>"
                f"Tier: {s['tier']}<br>"
                f"Fare: ₹{int(s['fare'])}<br>"
                f"Optical FOV: {s['fov_deg']}°<br>"
                f"Neck Tilt: {s['tilt']:.1f}°<br>"
                f"Dolby Immersion: {s['audio_immersion']:.0f}%"
            )

        fig.add_trace(go.Scatter3d(
            x=df["x"], y=df["y"], z=df["z"] + 0.35,
            mode="markers+text", text=df["seat_id"],
            textposition="top center", textfont=dict(color="#E2E8F0", size=9),
            marker=dict(size=sizes, color=colors, symbol=symbols, opacity=0.98, line=dict(color='#030712', width=1.5)),
            hovertext=hover_texts, hoverinfo="text", name="Seats"
        ))

        fig.update_layout(
            scene=dict(
                aspectmode='manual', aspectratio=dict(x=1.6, y=2.2, z=0.9),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="Depth"),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="Elevation"),
                bgcolor="#030712",
                camera=dict(eye=dict(x=0.0, y=-1.85, z=1.15), center=dict(x=0, y=0.1, z=-0.2), up=dict(x=0, y=0, z=1))
            ),
            updatemenus=[dict(
                type="buttons", direction="left", x=0.5, y=1.05, xanchor="center", yanchor="bottom",
                bgcolor="rgba(15, 23, 42, 0.9)", bordercolor="rgba(6, 182, 212, 0.45)", font=dict(color="#06B6D4", size=11),
                buttons=[
                    dict(label="🎥 Director 3D", method="relayout", args=[{"scene.camera.eye": dict(x=0.0, y=-1.85, z=1.15), "scene.camera.center": dict(x=0, y=0.1, z=-0.2)}]),
                    dict(label="📐 Top-Down 2D", method="relayout", args=[{"scene.camera.eye": dict(x=0.0, y=0.01, z=2.4), "scene.camera.center": dict(x=0, y=0.1, z=0)}]),
                    dict(label="👁️ Front Row POV", method="relayout", args=[{"scene.camera.eye": dict(x=0.0, y=-0.5, z=0.4), "scene.camera.center": dict(x=0, y=0.8, z=0.6)}]),
                ]
            )],
            margin=dict(l=0, r=0, t=35, b=0), height=500, paper_bgcolor="#030712", showlegend=False
        )
        return fig

    st.plotly_chart(render_customer_3d(seats_df, st.session_state.selected_seats), use_container_width=True)

    # Dolby Atmos 7.1.4 Surround Channel Visualizer HUD
    if st.session_state.selected_seats:
        hud_df = seats_df[seats_df["seat_id"].isin(st.session_state.selected_seats)]
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        h_col1, h_col2 = st.columns([1.5, 2.5])

        with h_col1:
            st.markdown("#### 🎧 Spatial Telemetry Readout")
            for _, s_row in hud_df.head(2).iterrows():
                st.markdown(f"""
                <div class="glass-card" style="padding:12px 14px; margin-bottom:8px; border:1px solid rgba(6, 182, 212, 0.3);">
                    <div style="font-size:13px; font-weight:800; color:#FACC15;">Seat {s_row['seat_id']} ({s_row['tier'].split('(')[0]})</div>
                    <div style="font-size:11px; color:#94A3B8;">Optical FOV: <b style="color:#06B6D4;">{s_row['fov_deg']}°</b> • Neck Tilt: <b style="color:#FFF;">{s_row['tilt']:.1f}°</b></div>
                    <div style="font-size:11px; color:#94A3B8;">Dolby Immersion: <b style="color:#10B981;">{s_row['audio_immersion']:.0f}%</b> • {s_row['spl_db']} dB SPL</div>
                </div>
                """, unsafe_allow_html=True)

        with h_col2:
            st.markdown("#### 🔊 Dolby Atmos 7.1.4 Surround Channel Spectrum")
            channels = ['Front Left', 'Center Dialogue', 'Front Right', 'Side Surround', 'Rear Surround', 'Overhead Top', 'LFE Subwoofer']
            avg_imm = hud_df["audio_immersion"].mean()
            # Dynamic speaker output simulation based on seat immersion
            levels = [
                avg_imm * 0.92, 94.0, avg_imm * 0.92,
                avg_imm * 0.85, avg_imm * 0.78, avg_imm * 0.95, 96.0
            ]
            fig_audio = go.Figure(go.Bar(
                x=channels, y=levels,
                marker=dict(color=['#06B6D4', '#FACC15', '#06B6D4', '#10B981', '#10B981', '#F43F5E', '#A855F7'])
            ))
            fig_audio.update_layout(
                height=180, margin=dict(l=5, r=5, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(range=[0, 100], title="Signal SPL %"), font=dict(color="#94A3B8", size=9)
            )
            st.plotly_chart(fig_audio, use_container_width=True)

    st.markdown("---")

    # Booking & Consolidated Checkout
    col_seat_cart, col_fnb_pay = st.columns([1.6, 1.6], gap="large")

    with col_seat_cart:
        st.subheader("💺 1. Choose Seats (All 96 Unlocked)")
        user_picks = st.multiselect("Select Any Seat:", options=all_seat_ids, default=st.session_state.selected_seats)
        st.session_state.selected_seats = user_picks

        st.markdown(f"""
        <div style="display:flex; justify-content:space-around; background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); padding:10px; border-radius:10px; margin-top:14px; font-size:12px;">
            <span style="color:#10B981;">🟢 <b>Prime Sweet Spot</b>: ₹{int(t_pricing['prime'] * effective_surge)}</span>
            <span style="color:#06B6D4;">🔵 <b>Standard Eye-Level</b>: ₹{int(t_pricing['standard'] * effective_surge)}</span>
            <span style="color:#F43F5E;">🔴 <b>Neck Relief Front</b>: ₹{int(t_pricing['front'] * effective_surge)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🚗 2. Multiplex Smart Parking Slot")
        parking_opt = st.radio("Add Reserved Parking?", ["No Parking Needed", "Two-Wheeler Slot (₹30)", "Car Valet Parking (₹80)"], horizontal=True)
        parking_cost = 80 if "Car" in parking_opt else 30 if "Two" in parking_opt else 0

    with col_fnb_pay:
        st.subheader("🍿 3. Multiplex Canteen & Delivery Option")
        fnb_delivery_mode = st.radio(
            "Snack Fulfillment:",
            ["🚀 Deliver Directly to Seat at Interval (+₹20)", "🏃 Express Counter Self-Pickup (Free)"],
            horizontal=True
        )
        delivery_charge = 20 if "Deliver Directly" in fnb_delivery_mode else 0

        fnb_col1, fnb_col2 = st.columns(2)
        with fnb_col1:
            popcorn_qty = st.number_input("Caramel Popcorn Tub (₹190)", min_value=0, max_value=6, value=1)
            nachos_qty = st.number_input("Peri-Peri Cheese Nachos (₹160)", min_value=0, max_value=6, value=0)
        with fnb_col2:
            coffee_qty = st.number_input("Cold Coffee Blast (₹120)", min_value=0, max_value=6, value=1)
            samosa_qty = st.number_input("Crispy Samosa Trio (₹90)", min_value=0, max_value=6, value=0)

        fnb_subtotal = (popcorn_qty * 190) + (nachos_qty * 160) + (coffee_qty * 120) + (samosa_qty * 90)
        fnb_total = fnb_subtotal + delivery_charge if fnb_subtotal > 0 else 0

        st.markdown("---")
        st.subheader("💳 4. Real-Time Consolidated Checkout")

        if user_picks:
            sel_records = seats_df[seats_df["seat_id"].isin(user_picks)]
            base_seat_amt = float(sel_records["fare"].sum())
            conv_fee = float(len(user_picks) * 22.0)
            gst = float(round((base_seat_amt + conv_fee + fnb_total) * 0.18, 2))
            grand_total = float(round(base_seat_amt + conv_fee + fnb_total + parking_cost + gst, 2))

            st.markdown(f"""
            <div class="gateway-box">
                <div class="invoice-line"><span>Seat Tickets ({len(user_picks)}):</span><strong>₹{int(base_seat_amt):,}</strong></div>
                <div class="invoice-line"><span>F&B Snacks Subtotal:</span><strong>₹{int(fnb_subtotal):,}</strong></div>
                {f'<div class="invoice-line"><span>Interval In-Seat Delivery Fee:</span><strong>₹{delivery_charge}</strong></div>' if delivery_charge > 0 and fnb_subtotal > 0 else ''}
                <div class="invoice-line"><span>Parking Slot:</span><strong>₹{int(parking_cost):,}</strong></div>
                <div class="invoice-line"><span>Convenience & GST (18%):</span><strong>₹{gst + conv_fee:.2f}</strong></div>
                <div class="invoice-total-line"><span>Grand Total:</span><span>₹{int(grand_total):,}</span></div>
            </div>
            """, unsafe_allow_html=True)

            pay_rail = st.radio("Payment Rail:", ["Google Pay", "PhonePe", "Paytm UPI", "Net Banking", "Cards"], horizontal=True)

            if st.button(f"⚡ Pay ₹{int(grand_total):,} via {pay_rail}", key="btn_pay_main"):
                with st.spinner("Authorizing Secure Fintech Rails..."):
                    time.sleep(1.0)
                    st.session_state.payment_done = True
                    st.session_state.txn_receipt = {
                        "theatre": sel_theatre_name, "audi": sel_audi, "genre": genre,
                        "slot": slot, "seats": ", ".join(user_picks), "total": int(grand_total),
                        "method": pay_rail, "txn_id": f"TXN-CBE-{int(time.time())}",
                        "fnb_items": f"{popcorn_qty} Popcorn, {coffee_qty} Coffee" if fnb_subtotal > 0 else "None",
                        "delivery_tag": "IN-SEAT DELIVERY" if delivery_charge > 0 and fnb_subtotal > 0 else "COUNTER PICKUP",
                        "parking": parking_opt.split('(')[0].strip(),
                        "food_token": f"FNB-{np.random.randint(100, 999)}" if fnb_subtotal > 0 else "NO-FNB",
                        "lat": t_meta["lat"], "lon": t_meta["lon"]
                    }
                    st.balloons()
                    st.rerun()

    # Digital Boarding Pass Display
    if st.session_state.payment_done and st.session_state.txn_receipt:
        rec = st.session_state.txn_receipt
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        r_left, r_right = st.columns([2.2, 1.2], gap="large")
        with r_left:
            st.markdown(f"""
            <div class="boarding-pass-wrap">
                <h3 style="color:#FACC15; margin:0; font-family:'Cinzel', serif;">{rec['theatre']}</h3>
                <p style="color:#94A3B8; font-size:13px; margin:4px 0 12px 0;">Confirmed Seats: <b style="color:#06B6D4;">{rec['seats']}</b> • Fare: <b style="color:#FACC15;">₹{rec['total']}</b> via {rec['method']}</p>
                <div style="background:rgba(255,255,255,0.04); padding:10px; border-radius:8px; font-size:12px; margin-bottom:8px;">
                    <div>🍿 <b>F&B Status:</b> <span style="color:#10B981; font-weight:700;">{rec['food_token']}</span> • {rec['delivery_tag']}</div>
                    <div>🚗 <b>Parking Verification:</b> {rec['parking']}</div>
                </div>
                <div style="font-size:11px; color:#64748B;">Turnstile Reference ID: <code>{rec['txn_id']}</code></div>
            </div>
            """, unsafe_allow_html=True)
        with r_right:
            qr = qrcode.QRCode(version=1, box_size=5, border=2)
            qr_content = f"TICKET|TXN={rec['txn_id']}|SEATS={rec['seats']}|THEATRE={rec['theatre']}|FNB={rec['food_token']}|TAG={rec['delivery_tag']}|PARK={rec['parking']}"
            qr.add_data(qr_content)
            qr.make(fit=True)
            buf = io.BytesIO()
            qr.make_image().save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Scan at Entrance Turnstile", width=170)

# =========================================================
# PORTAL 2: THEATRE MANAGEMENT & EXECUTIVE ANALYTICS
# =========================================================
elif st.session_state.selected_portal == "🏢 Theatre Manager Admin (BI)":
    st.subheader("🏢 Theatre Executive Management & Revenue Analytics")
    st.caption("Access restricted to Multiplex Operations, General Managers & Revenue Analysts.")

    if not st.session_state.admin_logged_in:
        auth_c1, auth_c2, auth_c3 = st.columns([1, 1.6, 1])
        with auth_c2:
            st.markdown("""
            <div class="glass-card" style="border:1px solid rgba(6,182,212,0.45); padding:24px; margin-top:20px;">
                <h3 style="color:#06B6D4; margin-top:0; font-family:'Cinzel', serif;">Manager Login Gateway</h3>
                <p style="color:#94A3B8; font-size:13px;">Enter the multiplex admin security passcode to unlock live yield controls and forecasting algorithms.</p>
            </div>
            """, unsafe_allow_html=True)

            passcode_in = st.text_input("Enter Passcode:", type="password", placeholder="Default: admin123")
            if st.button("Unlock Executive Dashboard", key="btn_login_admin"):
                if passcode_in in ["admin123", "cbe2026", "screensense"]:
                    st.session_state.admin_logged_in = True
                    st.success("Authorized! Loading real-time BI telemetry...")
                    st.rerun()
                else:
                    st.error("Invalid Manager Passcode. Please check your credentials.")
    else:
        st.sidebar.markdown("### ⚙️ Executive Yield Controls")
        new_multiplier = st.sidebar.slider(
            "Live Dynamic Pricing Multiplier:",
            0.85, 1.45, float(st.session_state.admin_dynamic_surge), 0.05
        )
        st.session_state.admin_dynamic_surge = new_multiplier

        if st.sidebar.button("🔒 Logout Manager Session"):
            st.session_state.admin_logged_in = False
            st.rerun()

        total_seats = len(seats_df)
        gross_potential = seats_df["fare"].sum()
        estimated_fnb_rev = int(total_seats * 0.75 * 140)
        sph_metric = (gross_potential * 0.75 + estimated_fnb_rev) / max(1, int(total_seats * 0.75))

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">76.4%</div><div class="kpi-label">Auditorium Projected Occupancy</div></div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{int(gross_potential * 0.76):,}</div><div class="kpi-label">Expected Box Office Yield</div></div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{int(estimated_fnb_rev):,}</div><div class="kpi-label">F&B Concession Run Rate</div></div>""", unsafe_allow_html=True)
        with k4:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{int(sph_metric):,}</div><div class="kpi-label">SPH (Spend Per Head Metric)</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)

        an_col1, an_col2 = st.columns(2)
        with an_col1:
            st.markdown("#### 🗺️ Spatial Seating Occupancy Density (Heatmap)")
            heat_pivot = seats_df.pivot(index="row", columns="col", values="historical_fill_rate")
            fig_h = px.imshow(
                heat_pivot, labels=dict(x="Column", y="Row", color="Fill %"),
                x=[str(i) for i in range(1, 13)], y=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                color_continuous_scale="Viridis"
            )
            fig_h.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0"))
            st.plotly_chart(fig_h, use_container_width=True)

        with an_col2:
            st.markdown("#### 🍿 Revenue Contribution Share (Tickets vs Concessions)")
            rev_share_fig = go.Figure(data=[go.Pie(
                labels=['Box Office Tickets', 'F&B Popcorn/Snacks', 'Convenience Fee', 'Parking Slots'],
                values=[gross_potential * 0.76, estimated_fnb_rev, 72 * 22, 72 * 35],
                hole=.45,
                marker=dict(colors=['#10B981', '#FACC15', '#06B6D4', '#F43F5E'])
            )])
            rev_share_fig.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0"))
            st.plotly_chart(rev_share_fig, use_container_width=True)

        st.markdown("---")

        # Dynamic Dead-Zone Auto-Repricer
        st.markdown("#### ⚡ Dead-Zone Auto-Repricer Simulation (Before vs After Optimization)")
        rep_col1, rep_col2 = st.columns([1.5, 2.5])
        with rep_col1:
            discount_sim = st.slider("Simulated Front-Row Discount (%):", 10, 50, 25, 5)
            original_front_rev = len(seats_df[seats_df["row"].isin(['A', 'B'])]) * 0.25 * t_pricing["front"]
            simulated_occupancy_boost = min(0.90, 0.25 + (discount_sim * 0.013))
            optimized_front_rev = len(seats_df[seats_df["row"].isin(['A', 'B'])]) * simulated_occupancy_boost * (t_pricing["front"] * (1 - discount_sim/100))

        with rep_col2:
            comp_fig = go.Figure(data=[
                go.Bar(name='Standard Flat Price', x=['Front Row Revenue (₹)'], y=[original_front_rev], marker_color='#F43F5E'),
                go.Bar(name='Algorithm Repriced', x=['Front Row Revenue (₹)'], y=[optimized_front_rev], marker_color='#10B981')
            ])
            comp_fig.update_layout(
                barmode='group', height=280, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0"), yaxis_title="Revenue (₹)"
            )
            st.plotly_chart(comp_fig, use_container_width=True)

        st.markdown("---")

        st.markdown("#### 🔮 14-Day Observed Box Office & 3-Day Predictive Forecast")
        dates_arr = pd.date_range(end=pd.Timestamp.now(), periods=14).strftime("%b %d")
        hist_rev = [42000, 48000, 39000, 52000, 78000, 96000, 91000, 44000, 47000, 41000, 58000, 89000, 104000, 98000]

        x_vals = np.arange(len(hist_rev))
        m, b = np.polyfit(x_vals, hist_rev, 1)
        future_proj = [m * (len(hist_rev) + i) + b for i in range(3)]
        proj_lbls = [f"Day +{i+1}" for i in range(3)]

        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=list(dates_arr), y=hist_rev, mode="lines+markers", name="Observed Box Office (₹)", line=dict(color="#06B6D4", width=3)))
        fig_p.add_trace(go.Scatter(x=proj_lbls, y=future_proj, mode="lines+markers", name="ML Forecast (₹)", line=dict(color="#FACC15", width=3, dash="dash")))
        fig_p.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Revenue (₹)", font=dict(color="#E2E8F0"), legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_p, use_container_width=True)

# =========================================================
# PORTAL 3: TURNSTILE SECURITY SCANNER (GATE STAFF VIEW)
# =========================================================
else:
    st.subheader("🛡️ Multiplex Speed-Gate Turnstile Staff Portal")
    st.caption("Live Gate Scanner terminal for entry verification and Canteen token validation.")

    scan_col1, scan_col2 = st.columns([1.5, 2.0], gap="large")

    with scan_col1:
        st.markdown("""
        <div class="glass-card" style="border:1px solid rgba(6,182,212,0.4);">
            <h4 style="color:#06B6D4; margin:0 0 8px 0;">Optical QR Ingestion</h4>
            <p style="color:#94A3B8; font-size:12px;">Paste or scan customer turnstile QR payload string below:</p>
        </div>
        """, unsafe_allow_html=True)

        demo_payload = f"TICKET|TXN=TXN-CBE-1738491|SEATS=E5, E6|THEATRE=Broadway Cinemas|FNB=FNB-482|TAG=IN-SEAT DELIVERY|PARK=Car Valet"
        scanned_input = st.text_area("Turnstile Scanner Payload:", value=demo_payload, height=120)

        verify_btn = st.button("🚀 Verify Pass & Unlock Speed-Turnstile")

    with scan_col2:
        if verify_btn and scanned_input:
            if "TICKET|TXN=" in scanned_input:
                tokens = dict(item.split("=") for item in scanned_input.split("|") if "=" in item)

                st.markdown(f"""
                <div style="background:rgba(16,185,129,0.12); border:2px solid #10B981; border-radius:14px; padding:20px; box-shadow:0 0 30px rgba(16,185,129,0.25);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 style="color:#10B981; margin:0; font-family:'Space Grotesk', sans-serif;">✅ ACCESS GRANTED</h2>
                        <span style="background:#10B981; color:#030712; padding:4px 10px; border-radius:6px; font-weight:800; font-size:12px;">TURNSTILE UNLOCKED</span>
                    </div>
                    <div style="margin-top:14px; font-size:14px; line-height:1.7;">
                        <div>Auditorium Gate: <b style="color:#FFF;">Gate 3 (Prime Sweet-Spot Access)</b></div>
                        <div>Validated Seats: <b style="color:#FACC15; font-size:18px;">{tokens.get('SEATS', 'N/A')}</b></div>
                        <div>Canteen Token: <b style="color:#06B6D4;">{tokens.get('FNB', 'NO-FNB')}</b> ({tokens.get('TAG', 'COUNTER')})</div>
                        <div>Parking Status: <b style="color:#FFF;">{tokens.get('PARK', 'None')}</b></div>
                        <div style="font-size:11px; color:#64748B; margin-top:8px;">Transaction Reference: <code>{tokens.get('TXN', 'VERIFIED')}</code></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:rgba(244,63,94,0.15); border:2px solid #F43F5E; border-radius:14px; padding:20px;">
                    <h3 style="color:#F43F5E; margin:0;">❌ ACCESS DENIED: INVALID QR PAYLOAD</h3>
                    <p style="color:#94A3B8; font-size:12px; margin-top:6px;">This QR barcode is forged, expired, or belongs to another showtime.</p>
                </div>
                """, unsafe_allow_html=True)