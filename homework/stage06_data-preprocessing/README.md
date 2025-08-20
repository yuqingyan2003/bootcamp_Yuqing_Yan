# Bootcamp Repository

## Folder Structure
- **homework/** → All homework contributions will be submitted here.
- **project/** → All project contributions will be submitted here.
- **class_materials/** → Local storage for class materials. Never pushed to
GitHub.

## Homework Folder Rules
- Each homework will be in its own subfolder (`homework0`, `homework1`, etc.)
- Include all required files for grading.

## Project Folder Rules
- Keep project files organized and clearly named.

## Data Storage Implementation (Stage 05)

### Directory Structure
data/
├── raw/ # Original immutable data (CSV format)
│ └── stock_data_YYYYMMDD_HHMMSS.csv
└── processed/ # Processed analysis-ready data (Parquet format)
└── stock_data_YYYYMMDD_HHMMSS.parquet

### Format Selection
| Format  | Location    | Purpose                          | Advantages                     |
|---------|------------|----------------------------------|--------------------------------|
| CSV     | data/raw/  | Raw data preservation            | Human-readable, universal      |
| Parquet | data/processed/ | Processed data storage     | Columnar, compressed, efficient |

### Environment Configuration
Configure these paths in `.env`:
```ini
DATA_DIR_RAW=data/raw
DATA_DIR_PROCESSED=data/processed
```
### Key Features
1. Automatic Path Handling
- Creates directories if missing using env variables

2. Validation Checks
- Shape consistency
- Column name matching
- Data type preservation
- Full data integrity

3. Utility Functions
```python
# Save with format detection
write_df(df, 'data/processed/final.parquet')
# Load with auto-parsing
df = read_df('data/processed/final.parquet')
```

## Data Cleaning Strategy

Use a modular and reproducible pipeline for data cleaning, implemented in `src/cleaning.py`:

- **Filling missing values:**
  - Numeric columns with missing values are filled using the median, which is robust to outliers and preserves the central tendency of the data.
  - Assumption: Missing values are missing at random; only numeric columns are filled.
  - Tradeoff: If missingness is not random, imputation may introduce bias or distort the distribution.

- **Dropping columns:**
  - Columns with more than 50% missing values are dropped to avoid analyses dominated by imputed data.
  - Assumption: Columns with excessive missingness are not useful for analysis.
  - Tradeoff: May result in loss of potentially valuable information if missingness is systematic.

- **Scaling numeric features:**
  - Numeric columns (e.g., 'price', 'volume') are scaled to the [0, 1] range using MinMaxScaler for comparability in machine learning tasks.
  - Assumption: Scaling is only applied to numeric columns.
  - Tradeoff: Original scale and interpretability are lost after scaling.

- **Visual comparison:**
  - Use visualizations (histograms, heatmaps) to compare the original and cleaned data, ensuring transparency and helping to identify any unintended effects of cleaning.

All cleaning steps are implemented as reusable functions, ensuring transparency and reproducibility for future datasets.