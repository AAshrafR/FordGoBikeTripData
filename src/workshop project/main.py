from analysis import (
    get_duration_by_gender,
    get_duration_by_user_type,
    get_top_routes,
    get_top_stations,
    plot_age_by_gender,
    plot_boxplots,
    plot_correlation_heatmap,
    plot_duration_by_user_type,
    plot_duration_hours_distribution,
)
from config import DATA_PATH, PROCESSED_DATA_PATH
from data_loading import (
    get_column_types,
    read_data,
)
from feature_engineering import add_all_features
from preprocessing import (
    check_nulls,
    check_outliers,
    converted_data_types,
    impute_missing_values,
    remove_outliers,
)


def export_cleaned_data(df, output_path):
  output_path.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(output_path, index=False)
  print(f"\n[SUCCESS] Cleaned data exported to: {output_path}")


def main():
  df = read_data(DATA_PATH)
  if df is None:
    print("Execution aborted: Could not load data.")
    return

  print("Data loaded successfully!")
  print(f"Initial Shape: {df.shape}")

  df_converted = converted_data_types(df)
  df_clean = impute_missing_values(df_converted)

  df_featured = add_all_features(df_clean, drop_old=True)

  df_final = remove_outliers(df_featured)
  print(f"\nFinal Cleaned Dataset Shape: {df_final.shape}")

  export_cleaned_data(df_final, PROCESSED_DATA_PATH)

  # 6. التحليل الإحصائي والتمثيل البياني (EDA)
  plot_duration_hours_distribution(df_final)
  plot_duration_by_user_type(df_final)

  print("\n--- Duration Stats by Gender ---")
  print(get_duration_by_gender(df_final))

  print("\n--- Duration Stats by User Type ---")
  print(get_duration_by_user_type(df_final))

  plot_age_by_gender(df_final)
  corr_matrix = plot_correlation_heatmap(df_final)

  print("\n--- Top 10 Start Stations ---")
  print(get_top_stations(df_final, top_n=10))

  print("\n--- Top 10 Routes ---")
  print(get_top_routes(df_final, top_n=10))


if __name__ == "__main__":
  main()