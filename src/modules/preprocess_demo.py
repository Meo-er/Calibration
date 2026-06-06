import pandas as pd
import numpy as np


def preprocess_demo(df_input, scaler, encoders, feature_columns):

    df = df_input.copy()
    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip()

    # convert numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Thay inf thành NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    # Đếm số dòng lỗi
    num_invalid = df.isnull().any(axis=1).sum()
    if num_invalid > 0:
        print(f"Đã loại bỏ {num_invalid} dòng chứa NaN hoặc Infinity.")
        df = df.dropna()
    if df.empty:
        print("Không còn dữ liệu hợp lệ để dự đoán.")
        return None

    # load encoder cũ nếu có
    for col, le in encoders.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col].astype(str))
            except ValueError:
                print(f"Cột '{col}' chứa giá trị chưa xuất hiện khi huấn luyện.")
                return None

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
