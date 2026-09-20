from pathlib import Path
import pandas as pd


def load_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load the Ford GoBike dataset from a CSV file.

    Parameters:
        file_path (str | Path): Path to the CSV dataset.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    return pd.read_csv(file_path)


def get_data_overview(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a column-level overview of the dataset.

    Parameters:
        df (pd.DataFrame): Input dataset.

    Returns:
        pd.DataFrame: Data type, non-null count, missing values,
        and unique-value count for each column.
    """
    return pd.DataFrame(
        {
            "Data Type": df.dtypes,
            "Non-Null Count": df.notna().sum(),
            "Missing Values": df.isna().sum(),
            "Unique Values": df.nunique(),
        }
    )
