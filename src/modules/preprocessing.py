from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


def preprocess_baseline(df_input):
    df = df_input.copy()

    # 1. Chuẩn hóa binary
    df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)
    print(f"Số cột còn lại: {df.shape[1]}")

    # 2. Encode
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if "Label" in cat_cols:
        cat_cols.remove("Label")
    if len(cat_cols) > 0:
        print(f"Đang encode các cột: {cat_cols}")
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    else:
        print("Không có cột phân loại nào cần encode.")

    # 3. Tách X, Y
    X = df.drop("Label", axis=1)
    y = df["Label"]

    # 4. Chia train/calibration/test (60/20/20)

    X_train_raw, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )

    X_cal_raw, X_test_raw, y_cal, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )

    # 5. Scale
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_cal = scaler.transform(X_cal_raw)
    X_test = scaler.transform(X_test_raw)
    print(f"Train: {X_train.shape}")
    print(f"Calibration: {X_cal.shape}")
    print(f"Test: {X_test.shape}")

    return X_train, X_cal, X_test, y_train, y_cal, y_test
