# Stock Insights: Predicting Apple Stock Trends with Data Science
**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement
Individual investors often lack the tools and expertise to analyze stock price trends and make data-driven predictions. This project addresses the challenge by building a reproducible pipeline that automatically collects, cleans, and analyzes daily stock data for Apple Inc. (AAPL) for the year 2023. The goal is to uncover historical price patterns, detect anomalies, and build a regression model to forecast future prices, thereby supporting smarter investment decisions.

## Stakeholder & User
- **Stakeholder:** Retail investors, financial bloggers, and educators seeking to empower individuals with better stock analytics.
- **User:** Individual investors who want to track, analyze, and forecast Apple stock performance as part of their investment workflow. Users interact with the output via notebooks, dashboards, or reports, typically before making buy/sell/hold decisions.

## Useful Answer & Decision
- **Descriptive:** What are the historical trends, volatility, and outliers in AAPL stock prices in 2023?
- **Predictive:** What is the expected closing price of AAPL in the next week/month, based on regression analysis?
- **Artifact:** Cleaned dataset, EDA visualizations, and a regression-based price prediction notebook. These outputs help users understand past performance and make informed buy/sell/hold decisions.

## Assumptions & Constraints
- Data is sourced from Yahoo Finance via yfinance, covering only daily OHLCV for AAPL in 2023.
- Missing values in numeric columns are filled with the median; columns with >50% missing are dropped.
- Outliers are detected using the IQR method and visualized with boxplots; extreme outliers may be removed or flagged.
- Data is assumed accurate as provided by the API; API access may be rate-limited or temporarily unavailable.
- The pipeline is for educational and personal use, not for professional trading.

## Known Unknowns / Risks
- API outages, changes, or deprecation.
- Missing or inconsistent data for certain dates.
- Unforeseen market events (e.g., splits, mergers) not reflected in the data.
- Model overfitting due to limited features or short timeframes.
- User misinterpretation of analytics as financial advice.

## Lifecycle Mapping
Goal → Stage → Deliverable
- Model problem with objective → Problem Framing & Scoping (Stage 01) → Data dictionary & methodology doc
- Constracture project environment → Tooling Setup (Stage 02) → yfinance collector with error handling, .gitignore, .env.example
- Achieve fundamental data-analyzing tools → Python Fundamentals (Stage 03) → Notebook with: momentum detection, sectoral decomposition
- Collect and store reliable stock data → Data Acquisition/Ingestion (Stage 04) → Raw CSV file
- Organize and validate data → Data Storage (Stage 05) → Raw/processed folders, format checks
- Clean and prepare data → Data Preprocessing (Stage 06) → Cleaning scripts, visual comparison
- Detect anomalies → Outlier Analysis (Stage 07) → Outlier report, boxplots
- Uncover trends and build predictive model → EDA & Modeling (Stage 08+) → EDA notebook, regression notebook, forecast artifact

## Repo Plan
- `/data/raw/`, `/data/processed/`: Store raw and cleaned stock data (CSV/Parquet)
- `/src/`: Acquisition, cleaning, and utility scripts (e.g., `acquisition.py`, `cleaning.py`, `utils.py`)
- `/notebooks/`: Jupyter notebooks for each project stage (acquisition, cleaning, EDA, regression, etc.)
- `/docs/`: Project documentation and slides
- `.gitignore`, `.env.example`: Ensure secrets and local configs are not committed
- **Update cadence:** Weekly during bootcamp, or as new features/data sources are added

## Data Cleaning Strategy
Use a modular and reproducible pipeline for data cleaning, implemented in `src/cleaning.py`:
- **Filling missing values:** Numeric columns are filled with the median (robust to outliers).
- **Dropping columns:** Columns with >50% missing values are dropped.
- **Scaling:** Numeric features are scaled to [0, 1] for comparability.
- **Outlier detection:** IQR method is used to flag or remove extreme values.
- **Visual comparison:** Distributions and missingness are visualized before and after cleaning.
All cleaning steps are implemented as reusable functions, ensuring transparency and reproducibility for future datasets.