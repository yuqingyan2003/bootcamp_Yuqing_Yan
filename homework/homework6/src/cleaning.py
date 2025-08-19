import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def fill_missing_median(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    df_filled = df.copy()
    for col in columns:
        if col in df.columns:
            df_filled[col] = df[col].fillna(df[col].median())
    return df_filled

def drop_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    missing_ratios = df.isnull().mean()
    cols_to_drop = missing_ratios[missing_ratios > threshold].index
    return df.drop(columns=cols_to_drop)

def normalize_data(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    df_norm = df.copy()
    scaler = MinMaxScaler()
    for col in columns:
        if col in df.columns:
            df_norm[col] = scaler.fit_transform(df[[col]])
    return df_norm