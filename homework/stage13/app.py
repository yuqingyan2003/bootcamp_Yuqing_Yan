"""
Flask API for AAPL Stock Price Prediction
"""
from flask import Flask, request, jsonify
import pickle
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the trained model
try:
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    """POST endpoint for prediction with JSON features"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features
        features = data.get('features', [])
        if len(features) != 6:
            return jsonify({'error': 'Expected 6 features: [open, high, low, volume, close_ma_5, price_range]'}), 400
        
        # Validate feature types
        try:
            features = [float(f) for f in features]
        except ValueError:
            return jsonify({'error': 'All features must be numeric'}), 400
        
        # Make prediction
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        prediction = model.predict([features])[0]
        
        return jsonify({
            'prediction': float(prediction),
            'features': features,
            'model_info': {
                'coefficients': model.coef_.tolist(),
                'intercept': float(model.intercept_)
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/predict/<float:open_price>', methods=['GET'])
def predict_single(open_price):
    """GET endpoint for single feature prediction"""
    try:
        if open_price < 0 or open_price > 1:
            return jsonify({'error': 'Open price must be between 0 and 1'}), 400
        
        # Use default values for other features
        features = [open_price, open_price + 0.1, open_price - 0.1, 0.5, open_price, 0.2]
        
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        prediction = model.predict([features])[0]
        
        return jsonify({
            'prediction': float(prediction),
            'open_price': open_price,
            'default_features_used': features
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/predict/<float:open_price>/<float:high_price>', methods=['GET'])
def predict_two(open_price, high_price):
    """GET endpoint for two feature prediction"""
    try:
        if open_price < 0 or open_price > 1 or high_price < 0 or high_price > 1:
            return jsonify({'error': 'Prices must be between 0 and 1'}), 400
        
        if high_price <= open_price:
            return jsonify({'error': 'High price must be greater than open price'}), 400
        
        # Use default values for other features
        low_price = open_price - 0.1
        features = [open_price, high_price, low_price, 0.5, open_price, high_price - low_price]
        
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        prediction = model.predict([features])[0]
        
        return jsonify({
            'prediction': float(prediction),
            'open_price': open_price,
            'high_price': high_price,
            'default_features_used': features
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/plot')
def plot():
    """GET endpoint to return a simple chart"""
    try:
        # Create a sample plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Sample data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        prices = np.linspace(0.5, 0.8, 50) + np.random.normal(0, 0.02, 50)
        
        ax.plot(dates, prices, linewidth=2, color='blue', alpha=0.7)
        ax.set_title('Sample AAPL Stock Price Trend', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Normalized Price')
        ax.grid(True, alpha=0.3)
        
        # Save plot to bytes
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_bytes = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return f'<img src="data:image/png;base64,{img_bytes}" style="max-width:100%; height:auto;"/>'
        
    except Exception as e:
        return jsonify({'error': f'Plot generation failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'endpoints': [
            'POST /predict',
            'GET /predict/<open_price>',
            'GET /predict/<open_price>/<high_price>',
            'GET /plot',
            'GET /health'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
