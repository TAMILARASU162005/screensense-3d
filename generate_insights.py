"""
ScreenSense 3D - Business Analytics & ROI Impact Engine
-------------------------------------------------------
Analyzes financial dead-zones, ergonomic churn, and revenue recovery lift.
Saves high-resolution analytic charts for business reporting and presentation.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

DATA_FILE = "cinema_pricing_training_data.csv"

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Missing '{DATA_FILE}'. Run train_model.py first.")

df = pd.read_csv(DATA_FILE)

# Set visual theme
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 11})

# --- Insight 1: Row-wise Occupancy vs Comfort Degradation ---
row_summary = df.groupby("row").agg(
    avg_comfort=("vci_score", "mean"),
    occupancy_rate=("is_booked", "mean"),
    avg_price=("target_price", "mean")
).reset_index()

plt.figure(figsize=(10, 5))
fig, ax1 = plt.subplots(figsize=(10, 5))

color = "tab:blue"
ax1.set_xlabel("Seat Row (Screen at Front: Row A)")
ax1.set_ylabel("Occupancy Rate (%)", color=color)
bars = ax1.bar(row_summary["row"], row_summary["occupancy_rate"] * 100, color=color, alpha=0.6, label="Fill Rate")
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("Visual Comfort Index (VCI / 100)", color=color)
ax2.plot(row_summary["row"], row_summary["avg_comfort"], color=color, marker="o", linewidth=2.5, label="Comfort Score")
ax2.tick_params(axis="y", labelcolor=color)

plt.title("The 'Dead Zone' Proof: Viewing Strain vs Seat Abandonment")
fig.tight_layout()
plt.savefig("insight_dead_zone_occupancy.png", dpi=300)
plt.close()

# --- Insight 2: Pricing Elasticity & Revenue Lift Calculation ---
# Simulation: Flat pricing (₹150 for all) vs Ergonomic Dynamic Pricing
df["flat_revenue"] = np.where(df["is_booked"] == 1, 150.0, 0.0)

# Under dynamic pricing: front row discounts increase booking rate by ~30%
simulated_dynamic_booked = df.apply(
    lambda r: 1 if (r["row"] in ["A", "B"] and np.random.rand() < 0.45) else r["is_booked"],
    axis=1
)
df["optimized_revenue"] = np.where(simulated_dynamic_booked == 1, df["target_price"], 0.0)

total_flat = df["flat_revenue"].sum()
total_optimized = df["optimized_revenue"].sum()
revenue_lift_pct = ((total_optimized - total_flat) / total_flat) * 100

print(f"--- Commercial Viability Report ---")
print(f"Traditional Flat Pricing Yield  : INR {total_flat:,.2f}")
print(f"ScreenSense Dynamic Optimization: INR {total_optimized:,.2f}")
print(f"Projected Monthly Revenue Lift  : +{revenue_lift_pct:.2f}%\n")
print("Visual charts saved: 'insight_dead_zone_occupancy.png'")