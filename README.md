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
