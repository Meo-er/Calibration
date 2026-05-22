import pandas as pd
import numpy as np

# readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
# df = pd.read_csv(readFile)


def data_cleaned_1(df_input: pd.DataFrame):
    df = df_input.copy()
    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip()
    # Chuẩn hóa nhãn
    df["Label"] = df["Label"].str.strip().str.upper()
    # convert numeric
    features = df.columns.drop("Label")
    for col in features:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print("LỌC DỮ LIỆU\n")
    print(f"Dữ liệu ban đầu: {df.shape}\n")
    # Xóa inf, nan
    print("-----Xử lý các giá trị bất thường (Infinity,NaN)-----")
    df = df.replace([np.inf, -np.inf], np.nan)
    print(f"Số lượng nhãn chứa giá trị vô cực và NaN: {df.isnull().any(axis=1).sum()}")
    nan_mask = df.isnull().any(axis=1)
    print(df.loc[nan_mask, "Label"].value_counts().rename_axis(None).to_string())
    print(f"Số dòng sẽ xóa: {df.isnull().any(axis=1).sum()} ")
    df = df.dropna()
    print(f"Số dòng còn lại: {df.shape[0]}\n")

    # Xóa dòng trùng
    print("-----Xử lý các dòng trùng lặp-----")
    print(f"Số dòng trùng: {df.duplicated().sum()}")
    duplicate_mask = df.duplicated()
    print(df.loc[duplicate_mask, "Label"].value_counts().rename_axis(None).to_string())
    print(f"Số dòng sẽ xóa: {df.duplicated().sum()}")
    df = df.drop_duplicates()
    print(f"Số dòng còn lại: {df.shape[0]}")
    print()

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
    print("-----Xử lý các cột không biến thiên-----")
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    print(f"Số cột không biến thiên: {len(constant_cols)}")
    print(f"Các cột sẽ xóa: {constant_cols}")
    df = df.drop(columns=constant_cols)
    print(f"\nSố dòng, cột còn lại: {df.shape}")

    return df


# df_cleaned = data_cleaned(df)
