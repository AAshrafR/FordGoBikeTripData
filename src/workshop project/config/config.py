from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "fordgobike-tripdataFor201902.csv"
file_path = DATA_PATH

PROCESSED_DATA_PATH = (
    BASE_DIR / "data" / "processed" / "fordgobike_cleaned.csv"
)

CATEGORICAL_COLS = ["user_type", "member_gender", "bike_share_for_all_trip"]
categorical_cols = CATEGORICAL_COLS

EXCLUDE_CORR_COLS = [
    "start_station_id",
    "end_station_id",
    "bike_id",
    "start_station_latitude",
    "start_station_longitude",
    "end_station_latitude",
    "end_station_longitude",
]

MAX_DURATION_MIN = 120.0
MAX_AGE = 80

AGE_BINS = [0, 25, 40, 100]
AGE_LABELS = ["Young", "Adult", "Senior"]

DURATION_BINS = [0, 10, 25, 60, 121]
DURATION_LABELS = [
    "Short (<10m)",
    "Medium (10-25m)",
    "Long (25-60m)",
    "Very Long (>60m)",
]


PALETTE_GENDER = {
    "Male": "#2b5c8f",
    "Female": "#e78ac3",
    "Other": "#fc8d62",
}
PALETTE_USER_TYPE = {
    "Subscriber": "#2b5c8f",
    "Customer": "#e66101",
}