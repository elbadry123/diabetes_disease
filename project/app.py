# app.py

import pickle
from flask import Flask, request, jsonify, render_template
import os
import json

# Initialize the Flask application
app = Flask(__name__)

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# JSON file to store predictions
predictions_file = os.path.join(os.path.dirname(__file__), 'predictions.json')

# Helper function to load/save predictions
def load_predictions():
    if os.path.exists(predictions_file):
        with open(predictions_file, 'r') as file:
            return json.load(file)
    return []

def save_predictions(predictions):
    with open(predictions_file, 'w') as file:
        json.dump(predictions, file, indent=4)

# Route to serve the index.html
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validate input data
    if not data or len(data) != 8:
        return jsonify({'error': 'Invalid input data'}), 400

    features = [data['Pregnancies'], data['Glucose'], data['BloodPressure'],
                data['SkinThickness'], data['Insulin'], data['BMI'],
                data['DiabetesPedigreeFunction'], data['Age']]

    # Make prediction
    prediction = model.predict([features])[0]

    # Save prediction and input data
    predictions = load_predictions()
    prediction_entry = {
        'input': data,
        'prediction': int(prediction)
    }
    predictions.append(prediction_entry)
    save_predictions(predictions)

    return jsonify({'prediction': int(prediction)})

# Route to display all predictions (Kanban View)
@app.route('/predictions')
def show_predictions():
    predictions = load_predictions()
    return render_template('kanban.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
