"""
ScreenSense 3D - Dynamic Pricing & ML Training Pipeline
-------------------------------------------------------
Generates synthetic cinema transaction data and trains a
RandomForestRegressor to predict optimal dynamic seat prices.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def generate_synthetic_booking_data(
    geometry_csv: str = "theater_seats_geometry.csv",
    num_shows: int = 50,
    random_state: int = 42
) -> pd.DataFrame:
    if not os.path.exists(geometry_csv):
        raise FileNotFoundError(
            f"'{geometry_csv}' not found. Run geometry_engine.py first."
        )

    np.random.seed(random_state)
    seats_df = pd.read_csv(geometry_csv)

    genres = ["Action", "Drama", "Horror", "Comedy", "Sci-Fi"]
    show_slots = ["Morning", "Matinee", "Evening", "Night"]
    day_types = ["Weekday", "Weekend"]

    records = []

    for show_id in range(1, num_shows + 1):
        genre = np.random.choice(genres, p=[0.35, 0.20, 0.15, 0.15, 0.15])
        slot = np.random.choice(show_slots, p=[0.15, 0.25, 0.35, 0.25])
        day = np.random.choice(day_types, p=[0.60, 0.40])

        slot_multiplier = {
            "Morning": 0.80,
            "Matinee": 0.95,
            "Evening": 1.25,
            "Night": 1.15
        }[slot]

        day_multiplier = 1.30 if day == "Weekend" else 1.00
        genre_eye_fatigue_factor = 1.20 if genre in ["Action", "Sci-Fi"] else 1.00
        base_theater_price = 150.0

        for _, seat in seats_df.iterrows():
            vci = seat["vci_score"]
            tilt = seat["vertical_tilt_deg"]

            effective_comfort = np.clip(100.0 - (100.0 - vci) * genre_eye_fatigue_factor, 0.0, 100.0)
            comfort_multiplier = 0.65 + (effective_comfort / 100.0) * 0.60

            booking_prob = (effective_comfort / 100.0) * 0.70 * (slot_multiplier * day_multiplier / 1.5)
            booking_prob = np.clip(booking_prob, 0.05, 0.98)
            booked = int(np.random.rand() < booking_prob)

            price = base_theater_price * comfort_multiplier * slot_multiplier * day_multiplier
            price += np.random.normal(0, 3.5)
            price = np.round(np.clip(price, 75.0, 300.0), 2)

            records.append({
                "show_id": show_id,
                "seat_id": seat["seat_id"],
                "row": seat["row"],
                "col": seat["col"],
                "pos_y": seat["pos_y"],
                "vertical_tilt_deg": tilt,
                "fov_horizontal_deg": seat["fov_horizontal_deg"],
                "yaw_deg": seat["yaw_deg"],
                "vci_score": vci,
                "genre": genre,
                "show_slot": slot,
                "day_type": day,
                "is_booked": booked,
                "target_price": price
            })

    return pd.DataFrame(records)


def train_pricing_model(data_df: pd.DataFrame, model_output_path: str = "pricing_model.pkl"):
    num_features = ["pos_y", "vertical_tilt_deg", "fov_horizontal_deg", "yaw_deg", "vci_score"]
    cat_features = ["genre", "show_slot", "day_type"]

    X = pd.get_dummies(data_df[num_features + cat_features], drop_first=True)
    y = data_df["target_price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    print(f"Model Trained! R2 Score: {r2:.4f} | MAE: INR {mae:.2f}")

    artifacts = {
        "model": model,
        "feature_columns": list(X.columns)
    }

    with open(model_output_path, "wb") as f:
        pickle.dump(artifacts, f)

    print(f"Exported model artifact to '{model_output_path}'")


if __name__ == "__main__":
    print("Generating training dataset...")
    dataset = generate_synthetic_booking_data(num_shows=60)
    dataset.to_csv("cinema_pricing_training_data.csv", index=False)
    print("Saved 'cinema_pricing_training_data.csv' successfully!")
    print("Training RandomForest model...")
    train_pricing_model(dataset)