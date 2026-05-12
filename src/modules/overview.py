import pandas as pd
import numpy as np


def data_overview(df):
    df.columns = df.columns.str.strip()
    print("DỮ LIỆU BAN ĐẦU")
    print()

    # Kích thước
    rows, cols = df.shape
    print(f"Số dòng: {rows} - Số cột: {cols}")
    print()

    # Nhãn
    unique_labels = df["Label"].unique().tolist()
    num_classes = len(unique_labels)
    print(f"Nhãn: {unique_labels} - Số lớp: {num_classes} ")
    classes_distribution = df["Label"].value_counts(normalize=True) * 100
    print("Phân bố:")
    for label, percent in classes_distribution.items():
        print(f"{label}: {percent:.2f}%")
    print()

    # Đặc trưng
    features_count = df.shape[1] - 1
    print(f"Số đặc trưng: {features_count}")
    features = df.drop(columns=["Label"])
    numerical_cols = features.select_dtypes(include=np.number).columns
    print(f"Đặc trưng số: {len(numerical_cols)}")
    categorical_cols = features.select_dtypes(exclude=np.number).columns
    print("Đặc trưng khác: ", end="")
    if len(categorical_cols) > 0:
        print({len(categorical_cols)})
        print(f"Danh sách: {categorical_cols.tolist()}")
    else:
        print("Không tồn tại")
    print()

    # Lỗi dữ liệu
    missing_values = df.isnull().sum()
    missing_dict = missing_values[missing_values > 0].to_dict()
    print(f"Giá trị thiếu: {missing_dict}")
    duplicate_count = df.duplicated().sum()
    print(f"Số dòng trùng: {duplicate_count}")
    inf_count = df.isin([np.inf, -np.inf]).sum()
    inf_dict = inf_count[inf_count > 0].to_dict()
    print(f"Số dòng chứa giá trị vô cực: {len(inf_dict)}")
    print()

    return df
