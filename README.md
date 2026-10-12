# 🎬 ScreenSense 3D: Cinema Ergonomic Seating & Dynamic Pricing Engine

An end-to-end Machine Learning and Spatial Ergonomics analytics system that calculates viewer neck strain and visual fatigue to optimize dynamic multiplex ticket pricing.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Machine Learning](https://img.shields.io/badge/Model-Random%20Forest%20Regressor-success)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit%20%26%20Plotly-orange)

---

## 📌 Problem Statement
In the multiplex industry, front rows (Rows A–C) suffer from chronic vacancy rates (>65% unbooked) due to severe vertical neck tilt, extreme horizontal viewing angles, and rapid visual fatigue. Flat pricing structures fail to capture consumer surplus for sweet-spot seating while simultaneously overpricing high-strain front rows, resulting in revenue dead-zones.

---

## 🚀 Key Solution Architecture

1. **3D Spatial Geometry Engine (`geometry_engine.py`)**:
   - Implements **SMPTE ST 199** and **THX Cinema Standards** to model screen coordinates and seating risers in 3D Euclidean space.
   - Vectorized trigonometric calculations compute:
     - **Vertical Neck Tilt ($\theta_v$)**: Deviation above horizontal sightlines.
     - **Horizontal Field of View (FOV)**: Lateral angular span of the display.
     - **Yaw Angle ($\theta_y$)**: Off-axis head rotation toward screen center.
   - Synthesizes an ergonomic benchmark score: **Visual Comfort Index (VCI)** ranging from 0 to 100.

2. **Dynamic Pricing Model (`train_model.py`)**:
   - Trains a **Random Forest Regressor** to model ticket price elasticity as a function of ergonomic comfort, genre-specific visual pacing (e.g., Action vs. Drama), time slots, and weekend surges.
   - **Performance:** Achieved **$R^2 = 0.99+$** and an MAE of under **₹3.00**.

3. **Business Impact & Dead-Zone Analytics (`generate_insights.py`)**:
   - Quantifies occupancy lift resulting from front-row ergonomic discounts.
   - Projects up to **15%–22% commercial occupancy recovery** in previously neglected front rows.

4. **Interactive Seating Heatmap (`app.py`)**:
   - A real-time **Streamlit + Plotly** interactive dashboard simulating dynamic ticket adjustments based on genre, slot, and occupancy surcharges.

---

## 🛠️ Project Structure

```bash
ScreenSense 3D/
├── geometry_engine.py             # 3D spatial trigonometry & ergonomic calculations
├── train_model.py                 # Synthetic data engine & Random Forest training
├── generate_insights.py           # Business analytics & dead-zone ROI reporting
├── app.py                         # Interactive Streamlit dashboard
├── theater_seats_geometry.csv     # Pre-calculated seat geometry metadata
├── cinema_pricing_training_data.csv # Synthetic transaction records
├── pricing_model.pkl              # Serialized ML model artifact
├── requirements.txt               # Environment dependencies
└── README.md                      # Project documentation