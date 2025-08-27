"""
Utility functions for AAPL stock analysis
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler

def calculate_metrics(df):
    """Calculate basic descriptive statistics"""
    return df.describe()

def engineer_features(df):
    """Engineer features for stock analysis"""
    df_copy = df.copy()
    
    # Price-based features
    df_copy['price_range'] = df_copy['High'] - df_copy['Low']
    df_copy['close_ma_5_prev'] = df_copy['Close'].shift(1).rolling(window=5, min_periods=5).mean()
    
    # Return-based features
    df_copy['ret'] = df_copy['Close'].pct_change()
    df_copy['lag_1'] = df_copy['ret'].shift(1)
    df_copy['roll_mean_5'] = df_copy['ret'].shift(1).rolling(5, min_periods=5).mean()
    df_copy['roll_vol_20'] = df_copy['ret'].shift(1).rolling(20, min_periods=20).std()
    
    return df_copy.dropna()

def train_model(X, y):
    """Train a linear regression model"""
    model = LinearRegression()
    model.fit(X, y)
    return model

def evaluate_model(model, X, y):
    """Evaluate model performance"""
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    
    return {
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'mae': mae,
        'predictions': y_pred
    }

def prepare_prediction_data(open_price, high_price, low_price, volume, close_ma_5):
    """Prepare data for prediction"""
    price_range = high_price - low_price
    return np.array([[open_price, high_price, low_price, volume, close_ma_5, price_range]])
