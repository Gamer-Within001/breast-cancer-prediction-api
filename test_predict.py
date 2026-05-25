import requests
import json
import numpy as np
from sklearn.datasets import load_breast_cancer

# Load a real sample from the dataset to ensure a valid prediction
data = load_breast_cancer()
# We will grab the first sample in the dataset (which happens to be malignant)
sample_features = data.data[0].tolist()

url = 'http://localhost:5000/predict'
payload = {'features': sample_features}

print("Sending patient data to Breast Cancer Prediction API...\n")

try:
    response = requests.post(url, json=payload)
    print("--- API Response ---")
    print(json.dumps(response.json(), indent=4))
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API. Make sure app.py is running.")