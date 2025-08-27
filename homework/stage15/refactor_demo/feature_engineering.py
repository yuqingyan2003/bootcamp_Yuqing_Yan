 #!/usr/bin/env python3
"""
AAPL Feature Engineering Task - CLI Refactor Demo
Stage 15: Orchestration & System Design

This script demonstrates converting a notebook-based feature engineering task
into a production-ready CLI function with logging, validation, and error handling.

Usage:
    python feature_engineering.py --input data/cleaned.csv --output data/features.csv
    python feature_engineering.py --input data/cleaned.csv --output data/features.csv --config config.json
"""

import argparse
import json
import logging
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
import time
import random
from functools import wraps


def retry_with_backoff(n_tries: int = 3, base_delay: float = 1.0, 
                      exponential: bool = True, jitter: bool = True,
                      exceptions: tuple = (Exception,)):
    """
    Enhanced retry decorator with exponential backoff and jitter.
    
    Args:
        n_tries: Maximum number of attempts
        base_delay: Base delay in seconds
        exponential: Use exponential backoff (2^attempt * base_delay)
        jitter: Add random jitter to prevent thundering herd
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(n_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < n_tries - 1:  # Don't delay on last attempt
                        if exponential:
                            delay = base_delay * (2 ** attempt)
                        else:
                            delay = base_delay
                        
                        if jitter:
                            delay += random.uniform(0, delay * 0.1)  # 0-10% jitter
                        
                        logging.warning(
                            f'[retry] Attempt {attempt + 1}/{n_tries} failed: {str(e)}. '
                            f'Retrying in {delay:.2f}s...'
                        )
                        time.sleep(delay)
                    else:
                        logging.error(
                            f'[retry] All {n_tries} attempts failed. Last error: {str(e)}'
                        )
            
            raise last_exception
        
        return wrapper
    return decorator


@retry_with_backoff(n_tries=2, base_delay=1.0, exceptions=(FileNotFoundError, PermissionError))
def feature_engineering_task(input_path: str, output_path: str, config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    AAPL Feature Engineering Task: Create technical indicators and derived features.
    
    Args:
        input_path: Path to cleaned AAPL data CSV
        output_path: Path to save features CSV
        config_path: Optional path to feature configuration JSON
        
    Returns:
        dict: Task execution summary with metrics
    """
    start_time = datetime.utcnow()
    logging.info('[feature_engineering] Starting feature engineering task')
    logging.info(f'[feature_engineering] Input: {input_path}')
    logging.info(f'[feature_engineering] Output: {output_path}')
    
    try:
        # Load configuration
        default_config = {
            'moving_average_window': 5,
            'volatility_window': 20,
            'price_range_enabled': True,
            'lagged_features_enabled': True,
            'validation_enabled': True,
            'target_variable': 'close_next'
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = {**default_config, **json.load(f)}
                logging.info(f'[feature_engineering] Loaded config from {config_path}')
        else:
            config = default_config
            logging.info('[feature_engineering] Using default configuration')
        
        # Validate input file
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Load data
        logging.info('[feature_engineering] Loading cleaned data')
        df = pd.read_csv(input_path, index_col='date', parse_dates=['date'])
        initial_rows = len(df)
        logging.info(f'[feature_engineering] Loaded {initial_rows} rows')
        
        # Validate required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Feature Engineering
        logging.info('[feature_engineering] Creating features')
        
        # 1. Price Range Feature
        if config['price_range_enabled']:
            df['price_range'] = df['High'] - df['Low']
            logging.info('[feature_engineering] Created price_range feature')
        
        # 2. Moving Average (previous days only, avoid leakage)
        ma_window = config['moving_average_window']
        df['close_ma_prev'] = df['Close'].shift(1).rolling(
            window=ma_window, min_periods=ma_window
        ).mean()
        logging.info(f'[feature_engineering] Created {ma_window}-day moving average')
        
        # 3. Returns and Lagged Features
        if config['lagged_features_enabled']:
            df['daily_return'] = df['Close'].pct_change()
            df['return_lag_1'] = df['daily_return'].shift(1)
            logging.info('[feature_engineering] Created return-based features')
        
        # 4. Volatility Features
        vol_window = config['volatility_window']
        df['rolling_volatility'] = df['daily_return'].shift(1).rolling(
            window=vol_window, min_periods=vol_window
        ).std()
        logging.info(f'[feature_engineering] Created {vol_window}-day rolling volatility')
        
        # 5. Target Variable (next day's close price)
        target_var = config['target_variable']
        if target_var == 'close_next':
            df['close_next'] = df['Close'].shift(-1)
        elif target_var == 'return_next':
            df['return_next'] = df['daily_return'].shift(-1)
        else:
            raise ValueError(f"Unknown target variable: {target_var}")
        
        logging.info(f'[feature_engineering] Created target variable ({target_var})')
        
        # Data Validation
        if config['validation_enabled']:
            logging.info('[feature_engineering] Performing data validation')
            
            # Check for data leakage in moving average
            if 'close_ma_prev' in df.columns:
                first_valid_ma = df['close_ma_prev'].first_valid_index()
                if first_valid_ma is not None:
                    expected_start_idx = ma_window
                    actual_start_idx = df.index.get_loc(first_valid_ma)
                    if actual_start_idx < expected_start_idx:
                        logging.warning('[feature_engineering] Potential data leakage in moving average')
            
            # Check feature correlations
            feature_cols = ['price_range', 'close_ma_prev', 'return_lag_1', 'rolling_volatility']
            available_features = [col for col in feature_cols if col in df.columns]
            
            correlations = {}
            if len(available_features) > 1:
                corr_matrix = df[available_features].corr()
                high_corr_pairs = []
                
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.8:
                            high_corr_pairs.append(
                                (corr_matrix.columns[i], corr_matrix.columns[j], corr_val)
                            )
                
                if high_corr_pairs:
                    logging.warning(f'[feature_engineering] High correlations detected: {high_corr_pairs}')
                else:
                    logging.info('[feature_engineering] Feature correlation validation passed')
                
                correlations = corr_matrix.to_dict()
        
        # Clean data (remove rows with NaN in target or key features)
        target_cols = [target_var] if target_var in df.columns else []
        required_for_modeling = available_features + target_cols
        
        initial_with_features = len(df)
        df_clean = df.dropna(subset=required_for_modeling)
        final_rows = len(df_clean)
        dropped_rows = initial_with_features - final_rows
        
        logging.info(f'[feature_engineering] Dropped {dropped_rows} rows with missing values')
        logging.info(f'[feature_engineering] Final dataset: {final_rows} rows')
        
        if final_rows == 0:
            raise ValueError("No valid rows remaining after feature engineering")
        
        # Save results
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save features CSV
        df_clean.to_csv(output_path, index=True, index_label='date')
        logging.info(f'[feature_engineering] Saved features to {output_path}')
        
        # Save feature metadata
        feature_info = {
            'task': 'feature_engineering',
            'created_features': available_features + target_cols,
            'config_used': config,
            'data_summary': {
                'initial_rows': initial_rows,
                'final_rows': final_rows,
                'dropped_rows': dropped_rows,
                'features_created': len(available_features),
                'date_range': {
                    'start': df_clean.index.min().isoformat(),
                    'end': df_clean.index.max().isoformat()
                }
            },
            'validation_results': {
                'feature_correlations': correlations if config['validation_enabled'] else None,
                'high_correlation_warnings': len(high_corr_pairs) if config['validation_enabled'] else 0
            },
            'execution_info': {
                'creation_time': start_time.isoformat(),
                'input_file': str(input_path),
                'output_file': str(output_path),
                'config_file': str(config_path) if config_path else None
            }
        }
        
        feature_info_path = output_dir / 'feature_info.json'
        with open(feature_info_path, 'w') as f:
            json.dump(feature_info, f, indent=2, default=str)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        logging.info(f'[feature_engineering] Task completed successfully in {duration:.2f} seconds')
        
        return {
            'status': 'success',
            'input_path': input_path,
            'output_path': output_path,
            'features_created': len(available_features) + len(target_cols),
            'rows_processed': final_rows,
            'duration_seconds': duration,
            'feature_info_path': str(feature_info_path),
            'config_used': config
        }
        
    except Exception as e:
        logging.error(f'[feature_engineering] Task failed: {str(e)}')
        return {
            'status': 'failed',
            'error': str(e),
            'input_path': input_path,
            'output_path': output_path,
            'duration_seconds': (datetime.utcnow() - start_time).total_seconds()
        }


def main(argv=None):
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AAPL Feature Engineering Task - Create technical indicators and derived features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input data/cleaned.csv --output data/features.csv
  %(prog)s --input data/cleaned.csv --output data/features.csv --config config.json --log-level DEBUG
  
Configuration File Example (JSON):
  {
    "moving_average_window": 5,
    "volatility_window": 20,
    "price_range_enabled": true,
    "lagged_features_enabled": true,
    "validation_enabled": true,
    "target_variable": "close_next"
  }
        """
    )
    
    parser.add_argument('--input', required=True, 
                       help='Path to cleaned AAPL data CSV')
    parser.add_argument('--output', required=True, 
                       help='Path to save features CSV')
    parser.add_argument('--config', 
                       help='Optional path to feature configuration JSON')
    parser.add_argument('--log-level', default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress output (errors still shown)')
    
    args = parser.parse_args(argv)
    
    # Setup logging
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    log_level = getattr(logging, args.log_level)
    
    if args.quiet:
        logging.basicConfig(level=logging.ERROR, format=log_format)
    else:
        logging.basicConfig(level=log_level, format=log_format, 
                          handlers=[logging.StreamHandler(sys.stdout)])
    
    # Validate input arguments
    if not Path(args.input).exists():
        print(f"❌ Error: Input file does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if args.config and not Path(args.config).exists():
        print(f"❌ Error: Config file does not exist: {args.config}", file=sys.stderr)
        sys.exit(1)
    
    # Execute task
    try:
        result = feature_engineering_task(args.input, args.output, args.config)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"❌ Feature engineering failed with unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    # Print summary and exit
    if result['status'] == 'success':
        if not args.quiet:
            print(f"\n✅ Feature engineering completed successfully!")
            print(f"   Features created: {result['features_created']}")
            print(f"   Rows processed: {result['rows_processed']}")
            print(f"   Duration: {result['duration_seconds']:.2f}s")
            print(f"   Output: {result['output_path']}")
            print(f"   Metadata: {result['feature_info_path']}")
        sys.exit(0)
    else:
        print(f"❌ Feature engineering failed: {result['error']}", file=sys.stderr)
        print(f"   Duration: {result['duration_seconds']:.2f}s", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()