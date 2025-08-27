 # Stage 15: Orchestration Plan - AAPL Stock Prediction Project

**Author**: Yuqing Yan  
**Date**: December 2024  
**Project**: AAPL Stock Price Prediction Pipeline  

## Executive Summary

This document outlines the orchestration strategy for the AAPL stock prediction project, breaking down the pipeline into 6 modular, reusable tasks with proper dependencies, logging, and automation decisions. The goal is to create a reliable, maintainable pipeline that can be executed consistently with minimal manual intervention.

---

## 1. Project Task Decomposition

### Pipeline Overview: 6 Core Tasks

| Task | Inputs | Outputs | Runtime | Idempotent |
|------|--------|---------|---------|------------|
| **data_ingestion** | yfinance API (AAPL, 2023-01-01 to 2023-12-31) | `data/raw/aapl_2023_raw.csv` | 2-5 min | ✅ Yes |
| **data_cleaning** | `data/raw/aapl_2023_raw.csv` | `data/processed/aapl_2023_cleaned.csv` | 1-2 min | ✅ Yes |
| **feature_engineering** | `data/processed/aapl_2023_cleaned.csv` | `data/processed/aapl_2023_features.csv` | 2-3 min | ✅ Yes |
| **model_training** | `data/processed/aapl_2023_features.csv` | `model/aapl_model.pkl + training_metrics.json` | 5-10 min | ❌ No* |
| **model_evaluation** | `model/aapl_model.pkl + test_data.csv` | `reports/model_evaluation.json + plots` | 3-5 min | ✅ Yes |
| **reporting** | `model/aapl_model.pkl + evaluation_results.json` | `deliverables/aapl_analysis.md + summary.pdf` | 2-3 min | ✅ Yes |

*Model training can be made idempotent by fixing random seeds

### Task Details

#### 1. Data Ingestion
- **Purpose**: Download AAPL stock data from Yahoo Finance
- **Key Operations**: API calls, data validation, format standardization
- **Failure Modes**: API rate limits, network timeouts, data format changes
- **Dependencies**: None (root task)

#### 2. Data Cleaning  
- **Purpose**: Clean, normalize, and validate raw stock data
- **Key Operations**: Missing value handling, outlier detection, data type conversion
- **Failure Modes**: Unexpected data formats, missing required columns
- **Dependencies**: data_ingestion

#### 3. Feature Engineering
- **Purpose**: Create technical indicators and derived features
- **Key Operations**: Moving averages, volatility calculation, lagged features
- **Failure Modes**: Calculation errors, data leakage, memory issues
- **Dependencies**: data_cleaning

#### 4. Model Training
- **Purpose**: Train Linear/Logistic Regression models
- **Key Operations**: Train-test split, model fitting, hyperparameter tuning
- **Failure Modes**: Convergence issues, insufficient data, overfitting
- **Dependencies**: feature_engineering

#### 5. Model Evaluation
- **Purpose**: Evaluate model performance with comprehensive metrics
- **Key Operations**: Prediction generation, metric calculation, diagnostic plots
- **Failure Modes**: Model loading errors, data format mismatches
- **Dependencies**: model_training

#### 6. Reporting
- **Purpose**: Generate stakeholder-ready analysis and documentation
- **Key Operations**: Report template processing, visualization generation
- **Failure Modes**: Template errors, file permission issues, formatting problems
- **Dependencies**: model_evaluation

---

## 2. Dependencies (DAG)

### Linear Pipeline Structure

```
data_ingestion → data_cleaning → feature_engineering → model_training → model_evaluation → reporting
```

### DAG Visualization

```
┌─────────────────┐
│ data_ingestion  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ data_cleaning   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│feature_engineer │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ model_training  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│model_evaluation │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   reporting     │
└─────────────────┘
```

### Dependency Rationale

- **Linear Structure**: Each task requires the complete output of the previous task
- **No Parallelization**: Current pipeline has sequential dependencies
- **Future Opportunities**: Model training could be parallelized across different algorithms
- **Critical Path**: Any task failure blocks all downstream tasks

### Potential Future Parallelization

1. **Multiple Model Training**: Train Linear Regression, Random Forest, XGBoost in parallel
2. **Multiple Evaluation Periods**: Evaluate on different time windows simultaneously  
3. **Multiple Report Formats**: Generate PDF, HTML, and PowerPoint reports in parallel

---

## 3. Logging & Checkpoints Strategy

### Centralized Logging Configuration

- **Log Level**: INFO for pipeline status, DEBUG for detailed operations
- **Log Format**: `[TIMESTAMP] [TASK] [LEVEL] MESSAGE`
- **Log Location**: `logs/{task_name}_YYYYMMDD_HHMMSS.log`
- **Log Retention**: 30 days for detailed logs, 1 year for summary logs
- **Aggregation**: All task logs collected in `logs/pipeline_summary.log`

### Task-Specific Logging Plan

| Task | Log Messages | Checkpoint Artifacts | Retry Policy |
|------|-------------|---------------------|--------------|
| **data_ingestion** | start/end timestamps, API calls, rows downloaded, data range, API errors | `data/raw/aapl_2023_raw.csv + ingestion_log.json` | 3 retries with exponential backoff |
| **data_cleaning** | start/end, input/output row counts, columns dropped, missing value stats | `data/processed/aapl_2023_cleaned.csv + cleaning_stats.json` | 2 retries with 1s delay |
| **feature_engineering** | start/end, features created, correlation stats, data leakage checks | `data/processed/aapl_2023_features.csv + feature_info.json` | 2 retries with 1s delay |
| **model_training** | start/end, hyperparameters, training metrics (R², RMSE), random seed | `model/aapl_model.pkl + training_metrics.json + config.json` | 1 retry with different seed |
| **model_evaluation** | start/end, test metrics, confusion matrix stats, prediction intervals | `reports/model_evaluation.json + plots/` | No retry (deterministic) |
| **reporting** | start/end, report sections generated, file sizes, artifacts created | `deliverables/ + generation_log.json` | 2 retries with 1s delay |

### Checkpoint Recovery Strategy

1. **Artifact Validation**: Each task validates input artifacts before processing
2. **Incremental Recovery**: Failed tasks can restart from last successful checkpoint
3. **Metadata Preservation**: All intermediate results include creation metadata
4. **Rollback Capability**: Previous successful artifacts are preserved with timestamps

---

## 4. Right-Sizing Automation

### Automate Now (Phase 1) - High Value, Low Risk

#### ✅ **Data Ingestion & Cleaning (Tasks 1-2)**
- **Rationale**: Well-defined, repetitive, high failure cost if done manually
- **Implementation**: CLI scripts with robust error handling and retry logic
- **ROI**: High - saves 30+ minutes per run, reduces human error
- **Timeline**: Immediate (Week 1)

#### ✅ **Feature Engineering (Task 3)**
- **Rationale**: Complex calculations prone to manual errors, time-consuming
- **Implementation**: Modular functions with comprehensive validation
- **ROI**: High - ensures consistency, enables rapid experimentation  
- **Timeline**: Immediate (Week 1)

#### ✅ **Model Evaluation (Task 5)**
- **Rationale**: Standard metrics, deterministic process, critical for decisions
- **Implementation**: Automated test suite with standard evaluation pipeline
- **ROI**: Medium-High - ensures consistent evaluation, reduces bias
- **Timeline**: Immediate (Week 2)

### Keep Manual for Now - Strategic Delays

#### 🔄 **Model Training (Task 4)**
- **Current State**: Semi-automated with manual hyperparameter tuning
- **Rationale**: Still experimenting with model types and parameters
- **Manual Review**: Human oversight required for training convergence
- **Automation Timeline**: Phase 2 (Next Month) once optimal parameters established

#### 🔄 **Reporting (Task 6)**  
- **Current State**: Template-based generation with manual content review
- **Rationale**: Requires human interpretation and stakeholder customization
- **Manual Review**: Content quality and business context validation
- **Automation Timeline**: Phase 3 (Future) - automate generation, keep review manual

### Automation Timeline & Risk Mitigation

**Phase 1 (Weeks 1-2)**: Core Data Pipeline
- Tasks: 1, 2, 3, 5 (Data flow + Evaluation)
- Risk Mitigation: Parallel manual verification during transition
- Success Criteria: 95% automation success rate

**Phase 2 (Month 2)**: Model Training Automation  
- Task: 4 (Model Training)
- Risk Mitigation: Human approval gates for training jobs
- Success Criteria: Consistent model quality without manual intervention

**Phase 3 (Future)**: Full Pipeline Automation
- Task: 6 (Automated reporting with human review)
- Risk Mitigation: Quality gates and manual override capabilities
- Success Criteria: End-to-end pipeline execution with minimal human input

### Automation Risk Controls

- **Manual Override**: All automated processes include emergency manual controls
- **Quality Gates**: Automated validation checks at each stage
- **Gradual Rollout**: Incremental automation with parallel manual verification
- **Rollback Plans**: Ability to revert to manual processes if automation fails

---

## 5. Implementation Roadmap

### Week 1: Core Automation Foundation
- [ ] Implement CLI wrapper for data ingestion task
- [ ] Implement CLI wrapper for data cleaning task  
- [ ] Implement CLI wrapper for feature engineering task
- [ ] Set up centralized logging infrastructure
- [ ] Create checkpoint validation system

### Week 2: Evaluation & Monitoring
- [ ] Implement CLI wrapper for model evaluation task
- [ ] Add comprehensive error handling and retry mechanisms
- [ ] Create pipeline monitoring dashboard
- [ ] Implement automated quality checks

### Week 3: Integration & Testing
- [ ] Create simple orchestration script for full pipeline
- [ ] Integration testing with real AAPL data
- [ ] Performance optimization and resource monitoring
- [ ] Documentation and runbook creation

### Week 4: Production Readiness
- [ ] Production deployment configuration
- [ ] Monitoring and alerting setup
- [ ] Training for manual override procedures
- [ ] Performance benchmarking and optimization

### Success Metrics

- **Reliability**: 95%+ successful pipeline runs
- **Efficiency**: 50%+ reduction in manual intervention time  
- **Maintainability**: Clear separation of concerns, modular design
- **Observability**: Complete audit trail of all pipeline executions
- **Recovery Time**: < 5 minutes to restart from any checkpoint

---

## 6. CLI Refactor Example: Feature Engineering

### Function Signature
```python
def feature_engineering_task(input_path: str, output_path: str, config_path: str = None) -> dict
```

### CLI Usage
```bash
python feature_engineering.py \
  --input data/processed/aapl_2023_cleaned.csv \
  --output data/processed/aapl_2023_features.csv \
  --config configs/feature_config.json \
  --log-level INFO
```

### Key Features
- **Comprehensive Logging**: Structured logging with timing and validation
- **Configuration Support**: JSON-based configuration for feature parameters
- **Data Validation**: Automatic checks for data leakage and quality issues
- **Error Handling**: Graceful failure with detailed error reporting
- **Metadata Generation**: Automatic creation of feature information files
- **Retry Support**: Integration with retry mechanisms for robustness

### Configuration Example
```json
{
  "moving_average_window": 5,
  "volatility_window": 20,
  "price_range_enabled": true,
  "lagged_features_enabled": true,
  "validation_enabled": true
}
```

---

## Conclusion

This orchestration plan provides a solid foundation for scaling the AAPL stock prediction project from manual notebook execution to a production-ready, automated pipeline. The phased approach to automation ensures risk management while delivering immediate value through improved reliability and efficiency.

The modular design with clear input/output contracts enables easy testing, debugging, and future enhancements. Comprehensive logging and checkpointing provide the observability needed for production operations.

**Next Action**: Begin implementation of Phase 1 automation (data pipeline tasks) with target completion in 2 weeks.