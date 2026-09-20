from pathlib import Path

# Dataset file name
DATA_FILE = "C:/Users/hp/Desktop/FordGoBikeTripData/FordGoBikeTripData/data/fordgobike-tripdataFor201902.csv"
OUTPUT_PATH = Path("C:/Users/hp/Downloads/ford_gobike_complete_project/data/fordgobike_cleaned.csv")
# Dataset-specific settings
DATA_YEAR = 2026
RANDOM_STATE = 42

# Columns used during preprocessing
DATETIME_COLUMNS = ["start_time", "end_time"]

INTEGER_COLUMNS = ["member_birth_year"]

CATEGORICAL_COLUMNS = [
    "start_station_id",
    "start_station_name",
    "end_station_id",
    "end_station_name",
    "user_type",
    "bike_id",
    "member_gender",
    "bike_share_for_all_trip",
]

# Main analysis columns
SPECIFIC_NUMERIC_COLUMNS = [
    "member_age",
    "trip_duration_min",
    "start_station_latitude",
    "start_station_longitude",
    "end_station_latitude",
    "end_station_longitude",
]

CORRELATION_COLUMNS = [
    "duration_sec",
    "member_birth_year",
    "member_age",
    "bike_id",
]
