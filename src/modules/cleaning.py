import pandas as pd
import numpy as np


def data_cleaned(df: pd.DataFrame):
    df.columns = df.columns.str.strip()
    df["Label"] = df["Label"].str.strip().str.upper()

    print("LỌC DỮ LIỆU\n")

    # Xóa dòng trùng
    print(f"Số dòng: {df.shape[0]} \nSố dòng trùng: {df.duplicated().sum()}")
    df = df.drop_duplicates()
    print(f"Số dòng sau khi xóa: {df.shape[0]}")
    print()

    # Xóa inf, nan
    features = df.columns.drop("Label")
    for col in features:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan)
    print(f"NaN trước xử lý: {df.isnull().sum().sum()}")
    df = df.dropna()
    print(f"Số dòng sau xử lý: {df.shape[0]}")
    print()

    # Chuẩn hóa binary
    df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

    # Xóa cột định danh
    cols_drop = [
        "Flow ID",
        "Source IP",
        "Destination IP",
        "Source Port",
        "Destination Port",
        "Timestamp",
    ]
    existing_cols = [c for c in cols_drop if c in df.columns]
    df = df.drop(columns=existing_cols)

    # Xóa cột không biến thiên
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    # print(f"Các cột đã xóa: {constant_cols}")
    df = df.drop(columns=constant_cols)

    # Xóa dòng chứa giá trị âm
    numeric_cols = df.select_dtypes(include=[np.number]).columns.to_list()
    if "Label" in numeric_cols:
        numeric_cols.remove("Label")
    negative_rows = ((df[numeric_cols] < 0).any(axis=1)).sum()
    print(f"Số dòng chứa giá trị âm: {negative_rows}")
    df = df[~(df[numeric_cols] < 0).any(axis=1)]
    print(f"Số dòng, cột còn lại: {df.shape}")
    print()
    return df
