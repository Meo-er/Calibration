import pandas as pd
import joblib

import os
import sys

# Lấy đường dẫn đến thư mục chứa chính file predict.py (tức là thư mục src)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Thêm thư mục src này vào danh sách tìm kiếm của Python
sys.path.append(current_dir)

# Bây giờ các dòng import bên dưới sẽ chạy bình thường
from modules.preprocess_demo import preprocess_demo

# Xác định đường dẫn tuyệt đối cho models
# File này là src/predict.py, nên models/ nằm ở src/models/
models_dir = os.path.join(current_dir, "models")

# Load
base_model = joblib.load(os.path.join(models_dir, "model_baseline.pkl"))
platt_model = joblib.load(os.path.join(models_dir, "model_platt.pkl"))
iso_model = joblib.load(os.path.join(models_dir, "model_iso.pkl"))
scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
encoders = joblib.load(os.path.join(models_dir, "encoders.pkl"))
feature_columns = joblib.load(os.path.join(models_dir, "features.pkl"))


def predict_flow(flow):

    # Convert thành dataframe
    df = pd.DataFrame([flow])
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Preprocess
    X = preprocess_demo(df, scaler, encoders, feature_columns)

    # Logistic Regression
    base_pred = base_model.predict(X)[0]
    base_prob = base_model.predict_proba(X)[0][1]

    # Platt Scaling
    platt_prob = platt_model.predict_proba(X)[0][1]

    # Isotonic
    iso_prob = iso_model.predict_proba(X)[0][1]

    return {
        "Logistic Regression": {
            "label": "ATTACK" if base_pred == 1 else "BENIGN",
            "prob": base_prob,
        },
        "Platt Scaling": {
            "label": "ATTACK" if platt_prob >= 0.5 else "BENIGN",
            "prob": platt_prob,
        },
        "Isotonic Regression": {
            "label": "ATTACK" if iso_prob >= 0.35 else "BENIGN",
            "prob": iso_prob,
        },
    }
