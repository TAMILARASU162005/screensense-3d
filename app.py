"""
ScreenSense 3D | Next-Gen Multiplex Operating System & BI Platform
===================================================================
- Photorealistic 3D Spatial Seating & Audio Immersion Engine (Dolby Atmos)
- Multiplex F&B Canteen Cart & Smart Parking Reservations
- Multi-Rail Fintech Checkout (UPI / Cards / Net Banking)
- Biometric QR Turnstile Boarding Pass with Food Token Integration
- Executive Management BI Dashboard: SPH (Spend Per Head) & Yield Elasticity
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
    page_title="ScreenSense 3D | Cinema OS & Analytics",
    page_icon="🎬",
    layout="wide"
)

# Custom High-End Obsidian & Champagne Gold Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0D1322 0%, #04060A 80%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #E2E8F0;
    }

    #MainMenu, header, footer {visibility: hidden;}

    .master-ribbon {
        background: linear-gradient(135deg, rgba(20, 26, 42, 0.95) 0%, rgba(8, 11, 18, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(90deg, #FFFFFF 0%, #F5D77F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .kpi-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #00F59B;
    }
    .kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #94A3B8;
        letter-spacing: 0.8px;
    }

    .gateway-box {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 20px;
        backdrop-filter: blur(14px);
    }
    .invoice-line {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        margin-bottom: 7px;
        color: #94A3B8;
    }
    .invoice-line strong { color: #F8FAFC; }
    .invoice-total-line {
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        margin-top: 12px;
        padding-top: 10px;
        display: flex;
        justify-content: space-between;
        font-size: 20px;
        font-weight: 700;
        color: #00F59B;
        font-family: 'Space Grotesk', sans-serif;
    }

    .boarding-pass-wrap {
        background: radial-gradient(circle at 10% 10%, #151D2F 0%, #080C14 100%);
        border: 1px solid rgba(212, 175, 55, 0.6);
        border-radius: 18px;
        padding: 26px;
        margin-top: 25px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85);
    }

    div.stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA820A 100%) !important;
        color: #05070B !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 22px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
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
    np.random.seed(42)

    for r_idx, r in enumerate(rows):
        dist_y = 3.6 + (r_idx * 2.5)
        elev_z = r_idx * 0.95
        tilt = np.degrees(np.arctan((6.8 - elev_z) / dist_y))

        for c in range(1, cols + 1):
            x_off = (c - (cols / 2 + 0.5)) * 1.5
            yaw = np.degrees(np.arctan(x_off / dist_y))
            vci = max(25, min(99, 100 - (abs(tilt - 13.5) * 2.3 + abs(yaw) * 1.6)))

            # Acoustic Telemetry Model (Dolby Atmos Reference Calibration)
            dist_center = np.sqrt(x_off**2 + (dist_y - 12.0)**2)
            audio_immersion = max(55, min(99, 100 - (dist_center * 2.8)))
            spl_db = round(85.0 - (dist_y * 0.45) + (elev_z * 0.3), 1)

            if r in ['A', 'B']:
                tier = "Ergonomic Discount (Front)"
                tier_key = "front"
                base_color = "#FF3366"
                occupancy_rate = np.random.uniform(0.18, 0.42)
            elif r in ['E', 'F', 'G']:
                tier = "Prime Sweet Spot (THX VIP)"
                tier_key = "prime"
                base_color = "#00F59B"
                occupancy_rate = np.random.uniform(0.88, 0.98)
            else:
                tier = "Standard Eye-Level"
                tier_key = "standard"
                base_color = "#FFB800"
                occupancy_rate = np.random.uniform(0.60, 0.82)

            seat_id = f"{r}{c}"
            status = "Sold Out" if np.random.rand() < occupancy_rate * 0.4 else "Available"
            if seat_id in ["E5", "E6"]:
                status = "Available"

            records.append({
                "seat_id": seat_id,
                "row": r,
                "col": c,
                "x": x_off,
                "y": dist_y,
                "z": elev_z,
                "tilt": tilt,
                "vci": vci,
                "audio_immersion": audio_immersion,
                "spl_db": spl_db,
                "tier": tier,
                "tier_key": tier_key,
                "base_color": base_color,
                "status": status,
                "historical_fill_rate": round(occupancy_rate * 100, 1)
            })

    return pd.DataFrame(records)

seats_df = load_multiplex_dataset()
bookable_seats = seats_df[seats_df["status"] != "Sold Out"]["seat_id"].tolist()

# ---------------------------------------------------------
# STATE INITIALIZATION
# ---------------------------------------------------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "selected_portal" not in st.session_state:
    st.session_state.selected_portal = "🎟️ Audience Booking Portal"
if "selected_seats" not in st.session_state:
    safe_init = [s for s in ["E5", "E6"] if s in bookable_seats] or bookable_seats[:2]
    st.session_state.selected_seats = safe_init
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "txn_receipt" not in st.session_state:
    st.session_state.txn_receipt = None
if "admin_dynamic_surge" not in st.session_state:
    st.session_state.admin_dynamic_surge = 1.05
if "global_theatre_name" not in st.session_state:
    st.session_state.global_theatre_name = "Broadway Cinemas - EPIQ (Avinashi Rd)"

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
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

# ---------------------------------------------------------
# GLOBAL PRICING & FARE CALCULATION
# ---------------------------------------------------------
active_surge = float(st.session_state.admin_dynamic_surge)
t_pricing = t_meta["pricing"]
seats_df["fare"] = seats_df["tier_key"].map(lambda k: round(t_pricing[k] * active_surge, 0))

# ---------------------------------------------------------
# TOP PORTAL SWITCHER RIBBON
# ---------------------------------------------------------
ribbon_left, ribbon_right = st.columns([2.5, 1.5])
with ribbon_left:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:28px;">🎬</span>
        <div>
            <h1 class="brand-title">SCREENSENSE 3D</h1>
            <div style="font-size:11px; color:#94A3B8; letter-spacing:1px;">COIMBATORE MULTIPLEX NETWORK & BI SUITE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with ribbon_right:
    portal_choice = st.radio(
        "Interface Mode:",
        ["🎟️ Audience Booking Portal", "🏢 Theatre Manager Admin (BI)"],
        horizontal=True,
        index=0 if st.session_state.selected_portal == "🎟️ Audience Booking Portal" else 1
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
            <h2 style="font-family:'Cinzel', serif; font-size:20px; color:#FFF; margin:0;">{sel_theatre_name.split(' - ')[0]}</h2>
            <p style="color:#94A3B8; font-size:12px; margin:3px 0 0 0;">📍 {t_meta['addr']} &nbsp;•&nbsp; 📽️ {sel_audi}</p>
        </div>
        <div>
            <a href="https://www.google.com/maps/search/?api=1&query={t_meta['lat']},{t_meta['lon']}" target="_blank" style="text-decoration:none;">
                <button style="background:rgba(212,175,55,0.15); border:1px solid #D4AF37; color:#F5D77F; padding:8px 16px; border-radius:8px; font-weight:700; cursor:pointer; font-size:12px;">
                    🧭 Live Google Maps
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3D Visualizer with Audio & Ergonomic Telemetry
    def render_customer_3d(df, selected_ids):
        fig = go.Figure()

        scr_x = np.linspace(-12, 12, 40)
        scr_z = np.linspace(1.8, 9.2, 20)
        X, Z = np.meshgrid(scr_x, scr_z)
        Y = -0.025 * (X**2)

        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale=[[0, '#8A7332'], [0.25, '#E8D595'], [0.5, '#FFFFFF'], [0.75, '#E8D595'], [1, '#8A7332']],
            showscale=False, name="Silver Screen", hoverinfo="name"
        ))

        for r_idx in range(len(df['row'].unique())):
            y_start = 3.2 + (r_idx * 2.5)
            z_height = r_idx * 0.95
            fig.add_trace(go.Mesh3d(
                x=[-11, 11, 11, -11, -11, 11, 11, -11],
                y=[y_start, y_start, y_start + 2.3, y_start + 2.3, y_start, y_start, y_start + 2.3, y_start + 2.3],
                z=[0, 0, 0, 0, z_height, z_height, z_height, z_height],
                color="#080C16", opacity=0.6, hoverinfo="skip"
            ))

        for sel_id in selected_ids:
            s_row = df[df["seat_id"] == sel_id]
            if not s_row.empty:
                s = s_row.iloc[0]
                fig.add_trace(go.Scatter3d(
                    x=[s["x"], 0], y=[s["y"], 0], z=[s["z"] + 0.5, 5.5],
                    mode="lines", line=dict(color="#D4AF37", width=5, dash="dot"), hoverinfo="skip"
                ))

        colors, sizes, symbols, hover_texts = [], [], [], []
        for _, s in df.iterrows():
            is_sel = s["seat_id"] in selected_ids
            st_val = s["status"]

            if is_sel:
                c, sz, sym, badge = "#D4AF37", 12, "circle", "⭐ [SELECTED]"
            elif st_val == "Sold Out":
                c, sz, sym, badge = "#2C3440", 6, "x", "❌ [BOOKED]"
            else:
                c, sz, sym, badge = s["base_color"], 8, "circle", "🟢 [AVAILABLE]"

            colors.append(c)
            sizes.append(sz)
            symbols.append(sym)
            hover_texts.append(
                f"<b>Seat: {s['seat_id']}</b> | {badge}<br>"
                f"Fare: ₹{int(s['fare'])}<br>"
                f"Neck Tilt: {s['tilt']:.1f}°<br>"
                f"Atmos Immersion: {s['audio_immersion']:.0f}%<br>"
                f"Sound SPL: {s['spl_db']} dB"
            )

        fig.add_trace(go.Scatter3d(
            x=df["x"], y=df["y"], z=df["z"] + 0.35,
            mode="markers+text", text=df["seat_id"],
            textposition="top center", textfont=dict(color="#CBD5E1", size=8),
            marker=dict(size=sizes, color=colors, symbol=symbols, opacity=0.96, line=dict(color='#04060A', width=1.2)),
            hovertext=hover_texts, hoverinfo="text", name="Seats"
        ))

        fig.update_layout(
            scene=dict(
                aspectmode='manual', aspectratio=dict(x=1.6, y=2.2, z=0.9),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="Depth"),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="Elevation"),
                bgcolor="#05070B",
                camera=dict(eye=dict(x=0.0, y=-1.85, z=1.15), center=dict(x=0, y=0.1, z=-0.2), up=dict(x=0, y=0, z=1))
            ),
            updatemenus=[dict(
                type="buttons", direction="left", x=0.5, y=1.05, xanchor="center", yanchor="bottom",
                bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="rgba(212, 175, 55, 0.4)", font=dict(color="#F5D77F", size=11),
                buttons=[
                    dict(label="🎥 Director 3D", method="relayout", args=[{"scene.camera.eye": dict(x=0.0, y=-1.85, z=1.15), "scene.camera.center": dict(x=0, y=0.1, z=-0.2)}]),
                    dict(label="📐 Top-Down 2D", method="relayout", args=[{"scene.camera.eye": dict(x=0.0, y=0.01, z=2.4), "scene.camera.center": dict(x=0, y=0.1, z=0)}]),
                    dict(label="👁️ Front Row POV", method="relayout", args=[{"scene.camera.eye": dict(x=0.0, y=-0.5, z=0.4), "scene.camera.center": dict(x=0, y=0.8, z=0.6)}]),
                ]
            )],
            margin=dict(l=0, r=0, t=35, b=0), height=500, paper_bgcolor="#05070B", showlegend=False
        )
        return fig

    st.plotly_chart(render_customer_3d(seats_df, st.session_state.selected_seats), use_container_width=True)

    # Interactive Inspection HUD for Chosen Seats
    if st.session_state.selected_seats:
        hud_df = seats_df[seats_df["seat_id"].isin(st.session_state.selected_seats)]
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        hud_cols = st.columns(min(len(hud_df), 4))
        for idx, (_, s_row) in enumerate(hud_df.head(4).iterrows()):
            with hud_cols[idx]:
                st.markdown(f"""
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08); padding:10px 14px; border-radius:10px;">
                    <div style="font-size:12px; font-weight:700; color:#D4AF37;">Seat {s_row['seat_id']} ({s_row['tier'].split('(')[0]})</div>
                    <div style="font-size:11px; color:#94A3B8;">Neck Tilt: <b style="color:#FFF;">{s_row['tilt']:.1f}°</b></div>
                    <div style="font-size:11px; color:#94A3B8;">Dolby Immersion: <b style="color:#00F59B;">{s_row['audio_immersion']:.0f}%</b> • {s_row['spl_db']} dB</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Seat Selection + Canteen Snacks + Smart Parking
    col_seat_cart, col_fnb_pay = st.columns([1.6, 1.6], gap="large")

    with col_seat_cart:
        st.subheader("💺 1. Choose Your Seats")
        user_picks = st.multiselect("Available Seats:", options=bookable_seats, default=st.session_state.selected_seats)
        st.session_state.selected_seats = user_picks

        st.markdown("### 🚗 2. Multiplex Smart Parking Slot")
        parking_opt = st.radio(
            "Add Reserved Parking Slot?",
            ["No Parking Needed", "Two-Wheeler Slot (₹30)", "Car Valet Parking (₹80)"],
            horizontal=True
        )
        parking_cost = 80 if "Car" in parking_opt else 30 if "Two" in parking_opt else 0

    with col_fnb_pay:
        st.subheader("🍿 3. Multiplex Canteen & Snacks Cart")
        fnb_col1, fnb_col2 = st.columns(2)
        with fnb_col1:
            popcorn_qty = st.number_input("Caramel Popcorn Tub (₹190)", min_value=0, max_value=6, value=1)
            nachos_qty = st.number_input("Peri-Peri Cheese Nachos (₹160)", min_value=0, max_value=6, value=0)
        with fnb_col2:
            coffee_qty = st.number_input("Cold Coffee Blast (₹120)", min_value=0, max_value=6, value=1)
            samosa_qty = st.number_input("Crispy Samosa Trio (₹90)", min_value=0, max_value=6, value=0)

        fnb_total = (popcorn_qty * 190) + (nachos_qty * 160) + (coffee_qty * 120) + (samosa_qty * 90)

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
                <div class="invoice-line"><span>Canteen & F&B Items:</span><strong>₹{int(fnb_total):,}</strong></div>
                <div class="invoice-line"><span>Parking Slot:</span><strong>₹{int(parking_cost):,}</strong></div>
                <div class="invoice-line"><span>Convenience & GST (18%):</span><strong>₹{gst + conv_fee:.2f}</strong></div>
                <div class="invoice-total-line"><span>Grand Total:</span><span>₹{int(grand_total):,}</span></div>
            </div>
            """, unsafe_allow_html=True)

            pay_rail = st.radio("Select Payment Method:", ["Google Pay", "PhonePe", "Paytm UPI", "Net Banking", "Cards"], horizontal=True)

            if st.button(f"⚡ Pay ₹{int(grand_total):,} via {pay_rail}", key="btn_pay_main"):
                with st.spinner("Authorizing Secure Fintech Rails..."):
                    time.sleep(1.0)
                    st.session_state.payment_done = True
                    st.session_state.txn_receipt = {
                        "theatre": sel_theatre_name, "audi": sel_audi, "genre": genre,
                        "slot": slot, "seats": ", ".join(user_picks), "total": int(grand_total),
                        "method": pay_rail, "txn_id": f"TXN-CBE-{int(time.time())}",
                        "fnb_items": f"{popcorn_qty} Popcorn, {coffee_qty} Coffee" if fnb_total > 0 else "None",
                        "parking": parking_opt.split('(')[0].strip(),
                        "food_token": f"FNB-{np.random.randint(100, 999)}" if fnb_total > 0 else "NO-FNB",
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
                <h3 style="color:#F5D77F; margin:0;">{rec['theatre']}</h3>
                <p style="color:#94A3B8; font-size:13px; margin:4px 0 12px 0;">Confirmed Seats: <b style="color:#D4AF37;">{rec['seats']}</b> • Fare: <b style="color:#00F59B;">₹{rec['total']}</b> via {rec['method']}</p>
                <div style="background:rgba(255,255,255,0.04); padding:10px; border-radius:8px; font-size:12px; margin-bottom:8px;">
                    <div>🍿 <b>Canteen Food Token:</b> <span style="color:#00F59B; font-weight:700;">{rec['food_token']}</span> ({rec['fnb_items']})</div>
                    <div>🚗 <b>Parking Verification:</b> {rec['parking']}</div>
                </div>
                <div style="font-size:11px; color:#64748B;">Turnstile Reference ID: <code>{rec['txn_id']}</code></div>
            </div>
            """, unsafe_allow_html=True)
        with r_right:
            qr = qrcode.QRCode(version=1, box_size=5, border=2)
            qr_content = f"TICKET|TXN={rec['txn_id']}|SEATS={rec['seats']}|THEATRE={rec['theatre']}|FNB={rec['food_token']}|PARK={rec['parking']}"
            qr.add_data(qr_content)
            qr.make(fit=True)
            buf = io.BytesIO()
            qr.make_image().save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Multiplex Speed-Gate Turnstile Pass", width=170)

# =========================================================
# PORTAL 2: THEATRE MANAGEMENT & EXECUTIVE ANALYTICS
# =========================================================
else:
    st.subheader("🏢 Theatre Executive Management & Revenue Analytics")
    st.caption("Access restricted to Multiplex Operations, General Managers & Revenue Analysts.")

    if not st.session_state.admin_logged_in:
        auth_c1, auth_c2, auth_c3 = st.columns([1, 1.6, 1])
        with auth_c2:
            st.markdown("""
            <div style="background:rgba(15,23,42,0.9); border:1px solid rgba(212,175,55,0.4); border-radius:14px; padding:24px; margin-top:20px;">
                <h3 style="color:#F5D77F; margin-top:0; font-family:'Cinzel', serif;">Manager Login Gateway</h3>
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
            0.85, 1.45, float(st.session_state.admin_dynamic_surge), 0.05,
            help="Alters active ticket rates across customer portals in real-time."
        )
        st.session_state.admin_dynamic_surge = new_multiplier

        if st.sidebar.button("🔒 Logout Manager Session"):
            st.session_state.admin_logged_in = False
            st.rerun()

        # Advanced Multiplex KPIs (Including SPH - Spend Per Head)
        sold_cnt = len(seats_df[seats_df["status"] == "Sold Out"])
        occ_ratio = (sold_cnt / len(seats_df)) * 100
        gross_ticket_yield = seats_df[seats_df["status"] == "Sold Out"]["fare"].sum()
        estimated_fnb_rev = sold_cnt * 140  # Industry average ₹140 per head
        sph_metric = (gross_ticket_yield + estimated_fnb_rev) / max(1, sold_cnt)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{occ_ratio:.1f}%</div><div class="kpi-label">Auditorium Occupancy</div></div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{int(gross_ticket_yield):,}</div><div class="kpi-label">Realized Box Office</div></div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{int(estimated_fnb_rev):,}</div><div class="kpi-label">F&B Canteen Concession Yield</div></div>""", unsafe_allow_html=True)
        with k4:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{int(sph_metric):,}</div><div class="kpi-label">SPH (Spend Per Head Metric)</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)

        an_col1, an_col2 = st.columns(2)

        with an_col1:
            st.markdown("#### 🗺️ Spatial Seating Occupancy Density (Heatmap)")
            st.caption("Identifies high-traffic acoustic sweet spots vs underperforming front rows.")
            heat_pivot = seats_df.pivot(index="row", columns="col", values="historical_fill_rate")
            fig_h = px.imshow(
                heat_pivot,
                labels=dict(x="Column", y="Row", color="Fill %"),
                x=[str(i) for i in range(1, 13)],
                y=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                color_continuous_scale="Viridis"
            )
            fig_h.update_layout(
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0")
            )
            st.plotly_chart(fig_h, use_container_width=True)

        with an_col2:
            st.markdown("#### 🍿 Revenue Contribution Share (Tickets vs F&B Concessions)")
            st.caption("Commercial multiplex profitability breakdown.")
            rev_share_fig = go.Figure(data=[go.Pie(
                labels=['Box Office Tickets', 'F&B Popcorn/Snacks', 'Convenience Fee', 'Parking Slots'],
                values=[gross_ticket_yield, estimated_fnb_rev, sold_cnt * 22, sold_cnt * 35],
                hole=.45,
                marker=dict(colors=['#00F59B', '#D4AF37', '#00E5FF', '#FFB800'])
            )])
            rev_share_fig.update_layout(
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0")
            )
            st.plotly_chart(rev_share_fig, use_container_width=True)

        st.markdown("---")

        st.markdown("#### 🔮 14-Day Observed Box Office & 3-Day Predictive Forecast")
        dates_arr = pd.date_range(end=pd.Timestamp.now(), periods=14).strftime("%b %d")
        hist_rev = [42000, 48000, 39000, 52000, 78000, 96000, 91000, 44000, 47000, 41000, 58000, 89000, 104000, 98000]

        x_vals = np.arange(len(hist_rev))
        m, b = np.polyfit(x_vals, hist_rev, 1)
        future_proj = [m * (len(hist_rev) + i) + b for i in range(3)]
        proj_lbls = [f"Day +{i+1}" for i in range(3)]

        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=list(dates_arr), y=hist_rev, mode="lines+markers", name="Observed Box Office (₹)", line=dict(color="#00F59B", width=3)))
        fig_p.add_trace(go.Scatter(x=proj_lbls, y=future_proj, mode="lines+markers", name="ML Forecast (₹)", line=dict(color="#FFB800", width=3, dash="dash")))
        fig_p.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Revenue (₹)", font=dict(color="#E2E8F0"), legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_p, use_container_width=True)