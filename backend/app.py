from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "delaney_solubility_with_descriptors.csv")

app = Flask(__name__)

FEATURES = ["MolLogP", "MolWt", "NumRotatableBonds", "AromaticProportion"]

MODELS = {
    "lr": joblib.load(os.path.join(BASE_DIR, "model", "linear_regression_model.pkl")),
    "rf": joblib.load(os.path.join(BASE_DIR, "model", "random_forest_model.pkl")),
}

MODEL_LABELS = {
    "lr": "Linear Regression",
    "rf": "Random Forest",
}

# Precompute dataset stats + scatter data once at startup so /scatter and the
# feature slider ranges don't touch the CSV on every request.
_df = pd.read_csv(DATA_PATH)
_X = _df[FEATURES]
_y = _df["logS"]

FEATURE_RANGES = {
    col: {
        "min": round(float(_X[col].min()), 3),
        "max": round(float(_X[col].max()), 3),
        "mean": round(float(_X[col].mean()), 3),
    }
    for col in FEATURES
}

_SCATTER_CACHE = {}
for key, model in MODELS.items():
    preds = model.predict(_X)
    _SCATTER_CACHE[key] = [
        [round(float(a), 3), round(float(p), 3)] for a, p in zip(_y, preds)
    ]

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

_x_train, _x_test, _y_train, _y_test = train_test_split(
    _X, _y, test_size=0.2, random_state=100
)

_METRICS_CACHE = {}
for key, model in MODELS.items():
    train_pred = model.predict(_x_train)
    test_pred = model.predict(_x_test)
    _METRICS_CACHE[key] = {
        "label": MODEL_LABELS[key],
        "train_mse": round(float(mean_squared_error(_y_train, train_pred)), 4),
        "train_r2": round(float(r2_score(_y_train, train_pred)), 4),
        "test_mse": round(float(mean_squared_error(_y_test, test_pred)), 4),
        "test_r2": round(float(r2_score(_y_test, test_pred)), 4),
    }

_LR_COEF = dict(zip(FEATURES, MODELS["lr"].coef_.tolist()))
_LR_INTERCEPT = float(MODELS["lr"].intercept_)
_RF_IMPORTANCE = dict(zip(FEATURES, MODELS["rf"].feature_importances_.tolist()))


@app.route("/")
def home():
    return render_template(
        "index.html",
        feature_ranges=FEATURE_RANGES,
        metrics=_METRICS_CACHE,
    )


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    model_key = data.get("model", "lr")

    if model_key not in MODELS:
        return jsonify({"error": f"unknown model '{model_key}'"}), 400

    try:
        values = [float(data[f]) for f in FEATURES]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "all four descriptors must be numbers"}), 400

    features = pd.DataFrame([values], columns=FEATURES)
    model = MODELS[model_key]
    prediction = model.predict(features)[0]

    return jsonify({
        "prediction": round(float(prediction), 4),
        "model": model_key,
    })


@app.route("/scatter")
def scatter():
    model_key = request.args.get("model", "lr")
    if model_key not in _SCATTER_CACHE:
        return jsonify({"error": f"unknown model '{model_key}'"}), 400
    return jsonify({
        "points": _SCATTER_CACHE[model_key],
        "metrics": _METRICS_CACHE[model_key],
    })


@app.route("/metrics")
def metrics():
    return jsonify({
        "metrics": _METRICS_CACHE,
        "lr_coefficients": _LR_COEF,
        "lr_intercept": _LR_INTERCEPT,
        "rf_importance": _RF_IMPORTANCE,
        "feature_ranges": FEATURE_RANGES,
    })


if __name__ == "__main__":
    app.run(debug=True)
