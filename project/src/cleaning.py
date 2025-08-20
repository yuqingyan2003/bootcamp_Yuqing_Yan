import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def fill_missing_median(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Fill missing values in specified columns with the median of each column.
    Assumption: Only numeric columns are passed. Median is robust to outliers.
    Args:
        df: Input DataFrame
        columns: List of columns to process
    Returns:
        DataFrame with filled missing values
    """
    df_filled = df.copy()
    for col in columns:
        if col in df.columns:
            df_filled[col] = df[col].fillna(df[col].median())
    return df_filled

def drop_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Drop columns with missing value ratio exceeding threshold.
    Assumption: Columns with too many missing values are not useful for analysis.
    Args:
        df: Input DataFrame
        threshold: Maximum allowed missing ratio (0-1)
    Returns:
        DataFrame with columns removed
    """
    missing_ratios = df.isnull().mean()
    cols_to_drop = missing_ratios[missing_ratios > threshold].index
    return df.drop(columns=cols_to_drop)

def normalize_data(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalize specified columns to [0,1] range using MinMaxScaler.
    Assumption: Only numeric columns are passed. Scaling improves ML performance.
    Args:
        df: Input DataFrame
        columns: List of columns to normalize
    Returns:
        DataFrame with normalized columns
    """
    df_norm = df.copy()
    scaler = MinMaxScaler()
    for col in columns:
        if col in df.columns:
            df_norm[col] = scaler.fit_transform(df[[col]])
    return df_norm
