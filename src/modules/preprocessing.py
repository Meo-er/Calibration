import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


def preprocess_baseline(df):
    # 1. Encode
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if "Label" in cat_cols:
        cat_cols.remove("Label")
    if len(cat_cols) > 0:
        # print(f"Đang encode các cột: {cat_cols}")
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = le.fit_transform(df[col].astype(str))
    else:
        print("Không có cột phân loại nào cần encode.")

    # 2. Tách X, Y
    X = df.drop("Label", axis=1)
    y = df["Label"]

    # 3. Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Chia train/calibration/test (60/20/20)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y, test_size=0.4, random_state=42, stratify=y
    )

    X_cal, X_test, y_cal, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    return X_train, X_cal, X_test, y_train, y_cal, y_test, scaler
