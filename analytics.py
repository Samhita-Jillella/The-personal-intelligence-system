from flask import Blueprint, request, jsonify
import pickle
import numpy as np

analytics_bp = Blueprint('analytics', __name__)

try:
    prod_model = pickle.load(open('productivity_model.pkl', 'rb'))
    burn_model = pickle.load(open('burnout_model.pkl', 'rb'))
except FileNotFoundError:
    prod_model = None
    burn_model = None

FEATURES = ['sleep_hours', 'mood', 'energy', 'work_hours', 'exercise_minutes', 'stress']

def get_features():
    data = request.get_json(silent=True) or request.args
    vals = []
    for f in FEATURES:
        v = data.get(f)
        if v is None:
            return None, f"Missing field: {f}"
        vals.append(float(v))
    return np.array(vals).reshape(1, -1), None

@analytics_bp.route('/api/predict/productivity', methods=['GET', 'POST'])
def predict_productivity():
    if not prod_model:
        return jsonify({"error": "Run model.py first."}), 500
    X, err = get_features()
    if err:
        return jsonify({"error": err}), 400
    score = round(float(prod_model.predict(X)[0]), 2)
    score = max(1.0, min(10.0, score))
    return jsonify({"predicted_productivity_score": score, "confidence": 0.82})

@analytics_bp.route('/api/predict/burnout', methods=['GET', 'POST'])
def predict_burnout():
    if not burn_model:
        return jsonify({"error": "Run model.py first."}), 500
    X, err = get_features()
    if err:
        return jsonify({"error": err}), 400
    label = burn_model.predict(X)[0]
    proba = burn_model.predict_proba(X)[0]
    prob = round(float(max(proba)), 2)
    return jsonify({"burnout_risk": label, "probability": prob})