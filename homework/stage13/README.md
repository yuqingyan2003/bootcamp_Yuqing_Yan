# AAPL Stock Price Prediction API

## Project Overview and Objectives

This project provides a machine learning API for predicting Apple Inc. (AAPL) stock prices based on historical market data. The model uses linear regression to predict normalized closing prices using engineered features including price ranges, moving averages, and return-based indicators.

### Key Features
- **Linear Regression Model**: Trained on 2023 AAPL stock data
- **Feature Engineering**: Price range, 5-day moving average, return-based features
- **RESTful API**: Multiple endpoints for different prediction scenarios
- **Error Handling**: Comprehensive input validation and error responses
- **Visualization**: Chart generation endpoint for data visualization

## How to Rerun Scripts/Notebooks

### Prerequisites
```bash
pip install -r requirements.txt
```

### Data Preparation
1. Ensure `project/data/processed/aapl_2023_cleaned.csv` exists
2. Run the notebook cells in order to:
   - Load and clean data
   - Engineer features
   - Train the model
   - Save model to `model/model.pkl`

### Model Training
```python
# The model is automatically trained when running the notebook
# Features used: ['Open', 'High', 'Low', 'Volume', 'close_ma_5_prev', 'price_range']
# Target: Normalized Close price
```

## Assumptions, Risks, and Lifecycle Mapping

### Assumptions
- **Data Quality**: Historical data is accurate and representative
- **Market Conditions**: 2023 market conditions are relevant for future predictions
- **Feature Relationships**: Linear relationships exist between features and target
- **Data Leakage**: No future information is used in feature engineering

### Risks
- **Market Volatility**: Stock markets are inherently unpredictable
- **Model Overfitting**: Linear model may not capture complex market dynamics
- **Data Drift**: Market conditions may change, reducing model accuracy
- **Feature Availability**: Some features may not be available in real-time

### Lifecycle Mapping
1. **Data Collection**: Daily stock data from reliable sources
2. **Feature Engineering**: Calculate technical indicators and price metrics
3. **Model Training**: Linear regression on historical data
4. **Model Deployment**: Flask API for real-time predictions
5. **Monitoring**: Track prediction accuracy and model performance
6. **Retraining**: Periodic model updates with new data

## Instructions for Using APIs or Dashboards

### Starting the API
```bash
python app.py
```
The API will be available at `http://localhost:5000`

### API Endpoints

#### 1. POST /predict
Predict stock price using JSON features.

**Request:**
```json
{
    "features": [0.5, 0.6, 0.4, 0.3, 0.55, 0.2]
}
```

**Response:**
```json
{
    "prediction": 0.523456,
    "features": [0.5, 0.6, 0.4, 0.3, 0.55, 0.2],
    "model_info": {
        "coefficients": [...],
        "intercept": 0.123
    }
}
```

#### 2. GET /predict/<open_price>
Predict using open price with default values for other features.

**Example:** `GET /predict/0.6`

#### 3. GET /predict/<open_price>/<high_price>
Predict using open and high prices with default values.

**Example:** `GET /predict/0.6/0.7`

#### 4. GET /plot
Generate and return a sample stock price chart.

#### 5. GET /health
Check API health and available endpoints.

### Error Handling
The API includes comprehensive error handling for:
- Missing or invalid input data
- Feature count mismatches
- Non-numeric features
- Model loading failures
- Invalid price ranges

### Testing the API
```python
import requests

# Test prediction endpoint
response = requests.post('http://localhost:5000/predict', 
                        json={'features': [0.5, 0.6, 0.4, 0.3, 0.55, 0.2]})
print(response.json())

# Test single feature endpoint
response = requests.get('http://localhost:5000/predict/0.6')
print(response.json())
```

## Project Structure
project/
├── app.py # Flask API application
├── model/
│ └── model.pkl # Trained model file
├── src/
│ └── utils.py # Utility functions
├── data/
│ └── processed/ # Processed data files
├── notebooks/ # Jupyter notebooks
├── requirements.txt # Python dependencies
└── README.md # This file


## Next Steps and Recommendations

### Short-term (1-3 months)
- Implement real-time data feeds
- Add more sophisticated models (Random Forest, Neural Networks)
- Create a web dashboard for interactive predictions
- Add model performance monitoring

### Medium-term (3-6 months)
- Implement ensemble methods for improved accuracy
- Add sentiment analysis from news and social media
- Create automated retraining pipelines
- Develop risk assessment metrics

### Long-term (6+ months)
- Expand to multiple stocks and markets
- Implement advanced time series models (LSTM, GRU)
- Add portfolio optimization features
- Create mobile applications

## Contact and Support
For questions or support, please refer to the project documentation or contact the development team.

---

**Disclaimer**: This model is for educational and research purposes only. Stock market predictions are inherently uncertain and should not be used as the sole basis for investment decisions. Always consult with financial professionals before making investment choices.
