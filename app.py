# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model and scaler at startup
try:
    model = joblib.load('svm_cancer_model.pkl')
    scaler = joblib.load('scaler.pkl')
    print("Model and scaler loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/', methods=['GET'])
def health_check():
    """Basic health check endpoint for monitoring script."""
    return jsonify({"status": "healthy", "service": "Breast Cancer Prediction API"})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions.
    Expects a JSON payload with a 'features' list containing 30 numeric values.
    """
    try:
        data = request.get_json()
        
        # Extract features
        if 'features' not in data:
            return jsonify({'error': 'Missing features in request data'}), 400
            
        features = np.array(data['features']).reshape(1, -1)
        
        # Ensure correct number of features (Breast Cancer dataset has 30)
        if features.shape[1] != 30:
            return jsonify({'error': f'Expected 30 features, got {features.shape[1]}'}), 400

        # Scale features and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)
        
        # Map prediction back to labels
        # In scikit-learn's dataset: 0 = Malignant, 1 = Benign
        diagnosis = "Benign (Non-cancerous)" if prediction[0] == 1 else "Malignant (Cancerous)"
        confidence = round(float(np.max(probability)) * 100, 2)

        return jsonify({
            'prediction': int(prediction[0]),
            'diagnosis': diagnosis,
            'confidence_percentage': confidence
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the application on all available IP interfaces on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)