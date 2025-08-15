# Inflation Dynamics Monitoring System
**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement
Current inflation reporting often fails to distinguish between temporary fluctuations and persistent trends, risking policy errors. For example, the Federal Reserve's delayed response to 2021 inflation resulted from over-reliance on headline CPI without analyzing sectoral drivers (Bernanke & Blanchard, 2023). This project creates an automated pipeline using Yahoo Finance's free API to:  
- Detect early signs of inflation acceleration/deceleration through 3-month annualized momentum metrics  
- Identify divergent trends between goods (PPI-sensitive) and services (wage-sensitive) inflation  
- Assess trend persistence using rolling volatility measures  
The system will help policymakers avoid two costly errors: tightening too late (letting inflation embed) or too early (unnecessary recessions).

## Stakeholder & User
- **Decision-makers:**  
  - FOMC voting members (set interest rates)  
  - Treasury debt management officials (adjust TIPS issuance)  
- **Primary Users:**  
  - Central bank research staff (prepare briefing materials)  
  - Bond market strategists (position duration exposure)  
- **Timing:**  
  - Data updates within 24 hours of BLS releases (10th each month)  
  - Alert triggers when:  
    - 3-mo momentum crosses ±1.5σ threshold  
    - Goods-services spread widens >200bps

## Useful Answer & Decision
- **Type:** Descriptive analytics with early-warning signals  
- **Metrics:**  
  - `Inflation Persistence Score` (rolling 6-mo autocorrelation)  
  - `Sectoral Divergence Index` (goods vs services impact)  
- **Artifacts:**  
  - Interactive Bokeh dashboard (inflation_nowcasting.html): displays CPI/PPI trends, sectoral breakdowns, and highlights early-warning signals for accelerating or decelerating inflation.
  - PDF summary report (inflation_trend_report.pdf): concise tear sheet summarizing trend regimes, sector-specific contributions, and notable regime shifts for policy or market use
- **Decision Impact:** Guides:  
  - Fed funds rate adjustments  
  - TIPS vs nominal Treasury issuance mix 

## Assumptions & Constraints
- **Data:**
  - Yahoo Finance maintains accurate CPI/PPI mappings (^CPIAUCSL, ^PPIACO)
  - Minimum 20-year history available for regime analysis
- **Analytical:**
  - Excludes food/energy volatility via core CPI focus

## Known Unknowns / Risks
- **Data Revisions Risk:** BLS back-revisions may alter trends → Maintain versioned raw data  
- **Proxy Accuracy:** Yahoo Finance vs BLS direct feeds → Weekly validation checks  
- **Structural Breaks:** COVID-era distortions → Manual override capability  
- **Geopolitical Shocks:** Sanctions impacts → Event annotation system  

## Lifecycle Mapping
Goal → Stage → Deliverable
- Problem Framing & Scoping → Stage 01 → Data dictionary & methodology doc  
- Build data pipeline → Stage 02 → yfinance collector with error handling  
- Develop analytics → Stage 03 → Notebook with:  
  - Momentum detection  
  - Sectoral decomposition  
- Deploy monitoring → Stage 04 → AWS Lambda scheduler  
- Refine alerts → Stage 05 → Markov regime switching model 

## Repo Plan
/data/
/raw/YYYYMMDD_CPI.csv
/processed/features.parquet
/src/
/data/collector.py
/analysis/regime_detection.py
/notebooks/
01_data_validation.ipynb
02_trend_analysis.ipynb
/docs/
bls_mapping.md
release_calendar.ics
...
