import numpy as np
import pandas as pd

def analyze_numeric(df, group_col=None):
    """
    Generate enhanced statistics for numeric columns.
    Compatible with both grouped and ungrouped data.
    """
    numeric_df = df.select_dtypes(include=np.number)
    
    if group_col and group_col in df.columns:
        stats = numeric_df.groupby(df[group_col]).agg(
            ['mean', 'std', 'min', 'max', 'count']
        )
    else:
        stats = numeric_df.describe(percentiles=[0.25, 0.5, 0.75])
        stats.loc['range'] = stats.loc['max'] - stats.loc['min']
    
    return stats