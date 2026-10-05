import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "traffic_forecasting_subset.csv"
FEATURE_FILE = PROJECT_ROOT / "data" / "traffic_forecasting_features.csv"

TRAIN_FILE = PROJECT_ROOT / "data" / "train.csv"
VALIDATION_FILE = PROJECT_ROOT / "data" / "validation.csv"
TEST_FILE = PROJECT_ROOT / "data" / "test.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

print("Loading traffic data...")
df = pd.read_csv(INPUT_FILE)

print(f"Initial rows: {len(df)}")


# ---------------------------------------------------------
# Create timestamp
# ---------------------------------------------------------

df["timestamp"] = pd.to_datetime(
    df[["Yr", "M", "D", "HH", "MM"]].rename(
        columns={
            "Yr": "year",
            "M": "month",
            "D": "day",
            "HH": "hour",
            "MM": "minute",
        }
    )
)

df["Vol"] = pd.to_numeric(df["Vol"], errors="coerce")


# ---------------------------------------------------------
# Sort observations
# ---------------------------------------------------------

df = df.sort_values(
    ["SegmentID", "Direction", "timestamp"]
).reset_index(drop=True)


# ---------------------------------------------------------
# Calendar features
# ---------------------------------------------------------

df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek


# ---------------------------------------------------------
# Lag features
#
# Data is sampled approximately every 15 minutes:
#
# lag_15  = previous 15 minutes
# lag_30  = previous 30 minutes
# lag_60  = previous 60 minutes
# lag_120 = previous 120 minutes
# lag_1day = previous day
# ---------------------------------------------------------

group_cols = ["SegmentID", "Direction"]

df["lag_15"] = (
    df.groupby(group_cols)["Vol"]
    .shift(1)
)

df["lag_30"] = (
    df.groupby(group_cols)["Vol"]
    .shift(2)
)

df["lag_60"] = (
    df.groupby(group_cols)["Vol"]
    .shift(4)
)

df["lag_120"] = (
    df.groupby(group_cols)["Vol"]
    .shift(8)
)

df["lag_1day"] = (
    df.groupby(group_cols)["Vol"]
    .shift(96)
)


# ---------------------------------------------------------
# Prediction target
#
# Predict traffic volume 15 minutes into the future.
# ---------------------------------------------------------

df["target_15min"] = (
    df.groupby(group_cols)["Vol"]
    .shift(-1)
)


# ---------------------------------------------------------
# Remove rows that cannot be used for modelling
# ---------------------------------------------------------

required_columns = [
    "Vol",
    "lag_15",
    "lag_30",
    "lag_60",
    "lag_120",
    "lag_1day",
    "target_15min",
]

df = df.dropna(subset=required_columns).reset_index(drop=True)


# ---------------------------------------------------------
# Save engineered feature dataset
# ---------------------------------------------------------

df.to_csv(FEATURE_FILE, index=False)

print(f"Feature dataset saved to: {FEATURE_FILE}")
print(f"Feature dataset rows: {len(df)}")


# ---------------------------------------------------------
df = df.sort_values("timestamp").reset_index(drop=True)

# Chronological train / validation / test split
#
# 70% train
# 15% validation
# 15% test
#
# IMPORTANT:
# We split chronologically to avoid future information
# leaking into the training data.
# ---------------------------------------------------------

n = len(df)

train_end = int(n * 0.70)
validation_end = int(n * 0.85)

train = df.iloc[:train_end].copy()
validation = df.iloc[train_end:validation_end].copy()
test = df.iloc[validation_end:].copy()


# ---------------------------------------------------------
# Save splits
# ---------------------------------------------------------

train.to_csv(TRAIN_FILE, index=False)
validation.to_csv(VALIDATION_FILE, index=False)
test.to_csv(TEST_FILE, index=False)


# ---------------------------------------------------------
# Report results
# ---------------------------------------------------------

print()
print("Chronological split complete:")
print(f"Train:      {len(train)} rows")
print(f"Validation: {len(validation)} rows")
print(f"Test:       {len(test)} rows")

print()
print("Train period:")
print(train["timestamp"].min(), "to", train["timestamp"].max())

print()
print("Validation period:")
print(validation["timestamp"].min(), "to", validation["timestamp"].max())

print()
print("Test period:")
print(test["timestamp"].min(), "to", test["timestamp"].max())

print()
print("Preprocessing complete.")
