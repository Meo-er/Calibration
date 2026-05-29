import pandas as pd
import numpy as np


def preprocess_demo(df_input, scaler, encoders, feature_columns):

    df = df_input.copy()
    # convert numeric
    features = df.columns.drop("Label", errors="ignore")
    for col in features:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # check inf,nan
    df = df.replace([np.inf, -np.inf], np.nan)
    if df[features].isnull().values.any():
        print("Input chứa giá trị thiếu hoặc vô cực. Vui lòng xử lý trước khi dự đoán.")
        return None

    # load encoder cũ nếu có
    for col, le in encoders.items():
        if col in df.columns:
            df[col] = le.transform(df[col].astype(str))

    # Check đủ cột
    missing_cols = set(feature_columns) - set(df.columns)
    if missing_cols:
        print(f"Cột còn thiếu: {missing_cols}")
        return None

    # Đúng thứ tự cột
    df = df[feature_columns]

    # Scale
    X_scaled = scaler.transform(df)

    return X_scaled
