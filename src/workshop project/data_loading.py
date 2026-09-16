from pathlib import Path
import pandas as pd
from config import DATA_PATH


def read_data(file_path: str | Path = DATA_PATH) -> pd.DataFrame | None:
  try:
    df = pd.read_csv(file_path)
    return df
  except FileNotFoundError:
    print(f"Error: The file at '{file_path}' was not found.")
  except pd.errors.EmptyDataError:
    print("Error: The file is empty.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  return None


def get_column_types(df: pd.DataFrame) -> dict:
  return {col: str(dtype) for col, dtype in df.dtypes.items()}