from pathlib import Path

from config import (
    DATA_FILE,
    OUTPUT_PATH,
    DATA_YEAR,
    CATEGORICAL_COLUMNS,
    INTEGER_COLUMNS,
)
from src.data_loading import load_data, get_data_overview
from src.preprocessing import (
    convert_to_nullable_integer,
    convert_to_category,
    handle_missing_values,
    remove_duplicates,
    add_time_validation_columns,
    handle_age_outliers,
)
from src.feature_engineering import (
    add_member_age,
    add_trip_duration_features,
    add_age_group,
)


def main() -> None:
    """Load, clean, and engineer the Ford GoBike dataset."""
    df = load_data(DATA_FILE)

    print("Original shape:", df.shape)
    print("\nInitial overview:")
    print(get_data_overview(df))

    # Preprocessing
    df = add_time_validation_columns(df)
    df = convert_to_nullable_integer(df, INTEGER_COLUMNS)
    df = convert_to_category(df, CATEGORICAL_COLUMNS)
    df = handle_missing_values(df)
    df = remove_duplicates(df)

    # 1. Feature Engineering: Calculate Member Age
    df = add_member_age(df, reference_year=DATA_YEAR)

    # 2. Preprocessing: Handle Age Outliers (Remove unrealistic ages)
    df = handle_age_outliers(df, min_age=12, max_age=80)

    # 3. Feature Engineering: Trip Duration & Age Grouping
    df = add_trip_duration_features(df)
    df = add_age_group(df)

    print("\nFinal shape:", df.shape)
    print("\nAverage age:", round(df["member_age"].mean(), 2))
    print("\nAge groups breakdown:")
    print(df["age_group"].value_counts())


    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nCleaned dataset saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()