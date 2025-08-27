"""
Evaluation and Risk Assessment Helper Functions
Stage 11: Evaluation & Risk Communication
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple, Callable, Any
import warnings

# Set default plotting style
plt.rcParams['figure.figsize'] = (10, 6)
sns.set_style("whitegrid")

class SimpleLinReg:
    """Simple Linear Regression implementation"""
    
    def fit(self, X, y):
        """Fit linear regression model"""
        X1 = np.c_[np.ones(len(X)), X.ravel()]
        beta = np.linalg.pinv(X1) @ y
        self.intercept_, self.coef_ = float(beta[0]), np.array([float(beta[1])])
        return self
    
    def predict(self, X):
        """Make predictions"""
        return self.intercept_ + self.coef_[0] * X.ravel()

def mean_impute(a: np.ndarray) -> np.ndarray:
    """Impute missing values with mean"""
    m = np.nanmean(a)
    out = a.copy()
    out[np.isnan(out)] = m
    return out

def median_impute(a: np.ndarray) -> np.ndarray:
    """Impute missing values with median"""
    m = np.nanmedian(a)
    out = a.copy()
    out[np.isnan(out)] = m
    return out

def zero_fill(a: np.ndarray) -> np.ndarray:
    """Fill missing values with zero"""
    return np.where(np.isnan(a), 0, a)

def forward_fill(a: np.ndarray) -> np.ndarray:
    """Forward fill missing values"""
    return pd.Series(a).fillna(method='ffill').fillna(method='bfill').values

def drop_missing(a: np.ndarray) -> np.ndarray:
    """Drop missing values"""
    return a[~np.isnan(a)] if np.isnan(a).any() else a

def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error"""
    return float(np.mean(np.abs(y_true - y_pred)))

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Square Error"""
    return float(np.sqrt(np.mean((y_true - y_pred)**2)))

def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """R-squared score"""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - (ss_res / ss_tot))

def bootstrap_metric(y_true: np.ndarray, y_pred: np.ndarray, 
                    metric_fn: Callable, n_boot: int = 500, 
                    seed: int = 111, alpha: float = 0.05) -> Dict[str, float]:
    """
    Bootstrap confidence interval for a metric
    
    Parameters:
    -----------
    y_true : array-like
        True values
    y_pred : array-like
        Predicted values
    metric_fn : callable
        Function to compute metric (e.g., mae, rmse)
    n_boot : int
        Number of bootstrap samples
    seed : int
        Random seed
    alpha : float
        Significance level for confidence interval
    
    Returns:
    --------
    dict : Dictionary with mean, lower, and upper confidence bounds
    """
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y_true))
    stats_list = []
    
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        try:
            stat = metric_fn(y_true[b], y_pred[b])
            stats_list.append(stat)
        except:
            continue
    
    if not stats_list:
        raise ValueError("No valid bootstrap samples generated")
    
    stats_array = np.array(stats_list)
    lo, hi = np.percentile(stats_array, [100*alpha/2, 100*(1-alpha/2)])
    
    return {
        'mean': float(np.mean(stats_array)),
        'lo': float(lo),
        'hi': float(hi),
        'std': float(np.std(stats_array))
    }

def bootstrap_predictions(X: np.ndarray, y: np.ndarray, x_grid: np.ndarray, 
                         n_boot: int = 500, seed: int = 111) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bootstrap confidence intervals for predictions
    
    Parameters:
    -----------
    X : array-like
        Training features
    y : array-like
        Training targets
    x_grid : array-like
        Grid of x values for prediction
    n_boot : int
        Number of bootstrap samples
    seed : int
        Random seed
    
    Returns:
    --------
    tuple : (mean_predictions, lower_ci, upper_ci)
    """
    rng = np.random.default_rng(seed)
    preds = []
    idx = np.arange(len(y))
    
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        try:
            m = SimpleLinReg().fit(X[b].reshape(-1,1), y[b])
            pred = m.predict(x_grid)
            preds.append(pred)
        except:
            continue
    
    if not preds:
        raise ValueError("No valid bootstrap predictions generated")
    
    P = np.vstack(preds)
    return P.mean(axis=0), np.percentile(P, 2.5, axis=0), np.percentile(P, 97.5, axis=0)

def bootstrap_coefficients(X: np.ndarray, y: np.ndarray, n_boot: int = 500, 
                          seed: int = 111) -> Dict[str, Dict[str, float]]:
    """
    Bootstrap confidence intervals for regression coefficients
    
    Parameters:
    -----------
    X : array-like
        Training features
    y : array-like
        Training targets
    n_boot : int
        Number of bootstrap samples
    seed : int
        Random seed
    
    Returns:
    --------
    dict : Dictionary with bootstrap results for intercept and slope
    """
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y))
    intercepts, slopes = [], []
    
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        try:
            m = SimpleLinReg().fit(X[b].reshape(-1,1), y[b])
            intercepts.append(m.intercept_)
            slopes.append(m.coef_[0])
        except:
            continue
    
    if not intercepts:
        raise ValueError("No valid bootstrap coefficients generated")
    
    intercepts = np.array(intercepts)
    slopes = np.array(slopes)
    
    return {
        'intercept': {
            'mean': float(np.mean(intercepts)),
            'lo': float(np.percentile(intercepts, 2.5)),
            'hi': float(np.percentile(intercepts, 97.5)),
            'std': float(np.std(intercepts))
        },
        'slope': {
            'mean': float(np.mean(slopes)),
            'lo': float(np.percentile(slopes, 2.5)),
            'hi': float(np.percentile(slopes, 97.5)),
            'std': float(np.std(slopes))
        }
    }

def fit_fn(X: np.ndarray, y: np.ndarray) -> SimpleLinReg:
    """Fit function for linear regression"""
    return SimpleLinReg().fit(X, y)

def pred_fn(model: SimpleLinReg, X: np.ndarray) -> np.ndarray:
    """Prediction function for linear regression"""
    return model.predict(X)

def scenario_sensitivity_analysis(X_raw: np.ndarray, y: np.ndarray, 
                                scenarios: Dict[str, Callable]) -> pd.DataFrame:
    """
    Perform scenario sensitivity analysis
    
    Parameters:
    -----------
    X_raw : array-like
        Raw features with potential missing values
    y : array-like
        Target values
    scenarios : dict
        Dictionary of scenario names and functions
    
    Returns:
    --------
    pd.DataFrame : Results for each scenario
    """
    results = []
    
    for name, fn in scenarios.items():
        try:
            if name == 'drop_missing' and np.isnan(X_raw).any():
                mask = ~np.isnan(X_raw)
                Xs, ys = X_raw[mask], y[mask]
                m = fit_fn(Xs.reshape(-1,1), ys)
                yh = m.predict(Xs.reshape(-1,1))
                mae_val = mae(ys, yh)
                rmse_val = rmse(ys, yh)
                r2_val = r2_score(ys, yh)
                n_obs = len(ys)
            else:
                Xs = fn(X_raw)
                m = fit_fn(Xs.reshape(-1,1), y)
                yh = m.predict(Xs.reshape(-1,1))
                mae_val = mae(y, yh)
                rmse_val = rmse(y, yh)
                r2_val = r2_score(y, yh)
                n_obs = len(y)
            
            results.append({
                'scenario': name,
                'mae': mae_val,
                'rmse': rmse_val,
                'r2': r2_val,
                'slope': m.coef_[0],
                'intercept': m.intercept_,
                'n_obs': n_obs
            })
        except Exception as e:
            warnings.warn(f"Scenario {name} failed: {e}")
            continue
    
    return pd.DataFrame(results)

def subgroup_diagnostics(df: pd.DataFrame, group_col: str, 
                        target_col: str, pred_col: str) -> pd.DataFrame:
    """
    Perform subgroup diagnostics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with predictions and residuals
    group_col : str
        Column name for grouping
    target_col : str
        Column name for target variable
    pred_col : str
        Column name for predictions
    
    Returns:
    --------
    pd.DataFrame : Group statistics
    """
    df_copy = df.copy()
    df_copy['residuals'] = df_copy[target_col] - df_copy[pred_col]
    
    # Group statistics
    group_stats = df_copy.groupby(group_col)['residuals'].agg([
        'count', 'mean', 'std', 'median', 'min', 'max'
    ]).round(4)
    
    # Statistical tests for group differences
    groups = df_copy[group_col].unique()
    group_tests = []
    
    for i, group1 in enumerate(groups):
        for group2 in groups[i+1:]:
            resid1 = df_copy[df_copy[group_col] == group1]['residuals'].values
            resid2 = df_copy[df_copy[group_col] == group2]['residuals'].values
            
            if len(resid1) > 1 and len(resid2) > 1:
                try:
                    t_stat, p_val = stats.ttest_ind(resid1, resid2)
                    group_tests.append({
                        'group1': group1,
                        'group2': group2,
                        't_stat': t_stat,
                        'p_value': p_val,
                        'significant': p_val < 0.05
                    })
                except:
                    continue
    
    return group_stats, pd.DataFrame(group_tests)

def create_diagnostic_plots(df: pd.DataFrame, group_col: str, 
                           target_col: str, pred_col: str, 
                           feature_col: str = None) -> None:
    """
    Create comprehensive diagnostic plots
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with data
    group_col : str
        Column name for grouping
    target_col : str
        Column name for target variable
    pred_col : str
        Column name for predictions
    feature_col : str, optional
        Column name for feature variable
    """
    df_copy = df.copy()
    df_copy['residuals'] = df_copy[target_col] - df_copy[pred_col]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # 1. Residuals vs Predicted
    axes[0, 0].scatter(df_copy[pred_col], df_copy['residuals'], alpha=0.6)
    axes[0, 0].axhline(y=0, color='red', linestyle='--')
    axes[0, 0].set_xlabel('Predicted Values')
    axes[0, 0].set_ylabel('Residuals')
    axes[0, 0].set_title('Residuals vs Predicted')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Residuals vs Feature (if provided)
    if feature_col:
        axes[0, 1].scatter(df_copy[feature_col], df_copy['residuals'], alpha=0.6)
        axes[0, 1].axhline(y=0, color='red', linestyle='--')
        axes[0, 1].set_xlabel(feature_col)
        axes[0, 1].set_ylabel('Residuals')
        axes[0, 1].set_title('Residuals vs Feature')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Residual Distribution
    axes[0, 2].hist(df_copy['residuals'], bins=20, alpha=0.7, edgecolor='black')
    axes[0, 2].set_xlabel('Residuals')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_title('Residual Distribution')
    axes[0, 2].grid(True, alpha=0.3)
    
    # 4. Residuals by Group (Boxplot)
    grouped = df_copy.groupby(group_col)['residuals']
    data = [s.values for _, s in grouped]
    labels = list(grouped.groups.keys())
    
    bp = axes[1, 0].boxplot(data, labels=labels, patch_artist=True)
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
    axes[1, 0].set_title('Residuals by Group')
    axes[1, 0].set_ylabel('Residuals')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 5. Residuals vs Predicted by Group
    for group in labels:
        group_data = df_copy[df_copy[group_col] == group]
        axes[1, 1].scatter(group_data[pred_col], group_data['residuals'], 
                           alpha=0.6, label=group, s=30)
    axes[1, 1].axhline(y=0, color='red', linestyle='--')
    axes[1, 1].set_xlabel('Predicted Values')
    axes[1, 1].set_ylabel('Residuals')
    axes[1, 1].set_title('Residuals vs Predicted by Group')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Residual Distribution by Group
    for group in labels:
        group_data = df_copy[df_copy[group_col] == group]
        axes[1, 2].hist(group_data['residuals'], alpha=0.5, label=group, bins=15)
    axes[1, 2].set_xlabel('Residuals')
    axes[1, 2].set_ylabel('Frequency')
    axes[1, 2].set_title('Residual Distribution by Group')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def create_scenario_comparison_plot(X_raw: np.ndarray, y: np.ndarray, 
                                   scenarios: Dict[str, Callable], 
                                   x_range: Tuple[float, float] = None) -> None:
    """
    Create scenario comparison plot
    
    Parameters:
    -----------
    X_raw : array-like
        Raw features
    y : array-like
        Target values
    scenarios : dict
        Dictionary of scenarios
    x_range : tuple, optional
        Range for x-axis
    """
    if x_range is None:
        x_range = (np.nanmin(X_raw), np.nanmax(X_raw))
    
    xg = np.linspace(x_range[0], x_range[1], 150).reshape(-1,1)
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    
    plt.figure(figsize=(12, 8))
    
    # Plot data points
    plt.scatter(X_raw, y, alpha=0.2, s=20, color='gray', label='Data Points')
    
    # Plot scenario fits
    for i, (name, fn) in enumerate(scenarios.items()):
        try:
            if name == 'drop_missing' and np.isnan(X_raw).any():
                mask = ~np.isnan(X_raw)
                Xi, yi = X_raw[mask], y[mask]
            else:
                Xi, yi = fn(X_raw), y
            
            m = fit_fn(Xi.reshape(-1,1), yi)
            color = colors[i % len(colors)]
            plt.plot(xg, m.predict(xg), color=color, 
                    label=f"{name} (slope: {m.coef_[0]:.3f})", 
                    linewidth=2)
        except Exception as e:
            warnings.warn(f"Failed to plot scenario {name}: {e}")
            continue
    
    plt.xlabel('X Feature')
    plt.ylabel('Y Target')
    plt.title('Scenario Fits Comparison')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def create_metric_comparison_plot(sensitivity_results: pd.DataFrame, 
                                 baseline_metric: float = None) -> None:
    """
    Create metric comparison plot
    
    Parameters:
    -----------
    sensitivity_results : pd.DataFrame
        Results from sensitivity analysis
    baseline_metric : float, optional
        Baseline metric value for comparison
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # MAE comparison
    scenario_names = sensitivity_results['scenario']
    mae_values = sensitivity_results['mae']
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
    
    bars1 = ax1.bar(scenario_names, mae_values, color=colors[:len(scenario_names)], alpha=0.7)
    if baseline_metric is not None:
        ax1.axhline(y=baseline_metric, color='red', linestyle='--', 
                    label=f'Baseline MAE: {baseline_metric:.4f}')
    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('MAE')
    ax1.set_title('MAE by Scenario')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars1, mae_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001, 
                 f'{value:.4f}', ha='center', va='bottom')
    
    # RMSE comparison
    rmse_values = sensitivity_results['rmse']
    bars2 = ax2.bar(scenario_names, rmse_values, color=colors[:len(scenario_names)], alpha=0.7)
    ax2.set_xlabel('Scenario')
    ax2.set_ylabel('RMSE')
    ax2.set_title('RMSE by Scenario')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars2, rmse_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001, 
                 f'{value:.4f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()