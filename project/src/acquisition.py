import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start, end, save_path):
    """
    Fetch historical stock data from Yahoo Finance and save as CSV.
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        start (str): Start date (YYYY-MM-DD)
        end (str): End date (YYYY-MM-DD)
        save_path (str): Path to save CSV file
    Returns:
        pd.DataFrame: Downloaded stock data
    """
    df = yf.download(ticker, start=start, end=end)
    df.to_csv(save_path)
    return df
