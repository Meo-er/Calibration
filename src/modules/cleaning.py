import pandas as pd
import numpy as np

# readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
# df = pd.read_csv(readFile)


def data_cleaned(df_input: pd.DataFrame):
    df = df_input.copy()
    df.columns = df.columns.str.strip()
    df["Label"] = df["Label"].str.strip().str.upper()

    print("LỌC DỮ LIỆU\n")

    # Xóa dòng trùng
    print(f"Số dòng: {df.shape[0]} \nSố dòng trùng: {df.duplicated().sum()}")
    duplicate_mask = df.duplicated()

    print(df.loc[duplicate_mask, "Label"].value_counts())
    df = df.drop_duplicates()
    print(f"Số dòng sau khi xóa: {df.shape[0]}")
    print()

    # convert numeric
    features = df.columns.drop("Label")
    for col in features:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Xóa inf, nan
    df = df.replace([np.inf, -np.inf], np.nan)
    print(f"Số dòng chứa NaN trước xử lý: {df.isnull().any(axis=1).sum()}")
    df = df.dropna()
    print(f"Số dòng chứa NaN sau xử lý: {df.shape[0]}")
    print()

    # Xóa dòng chứa giá trị âm
    numeric_cols = df.select_dtypes(include=[np.number]).columns.to_list()
    if "Label" in numeric_cols:
        numeric_cols.remove("Label")
    negative_count = (df[numeric_cols] < 0).sum()
    negative_count = negative_count[negative_count > 0]
    print(
        f"Các cột chứa giá trị âm: \n{negative_count.sort_values(ascending=False).to_string()}"
    )

    # ép Flow IAT Min về 0 nếu âm vì gói tin có thể đến cùng lúc
    if "Flow IAT Min" in df.columns:
        df["Flow IAT Min"] = df["Flow IAT Min"].clip(lower=0)

    fix_negative_cols = [
        "Flow IAT Mean",
        "Flow IAT Max",
        "Flow Packets/s",
    ]

    for col in fix_negative_cols:
        if col in df.columns:

            positive_values = df.loc[df[col] >= 0, col]
            if len(positive_values) > 0:
                median_value = positive_values.median()
                negative_mask = df[col] < 0
                if negative_mask.sum() > 0:
                    df.loc[negative_mask, col] = median_value
                    print(
                        f"  Fix {col}: {negative_mask.sum()} dòng → median = {median_value:.4f}"
                    )
            else:
                print(f"   {col}: Không có giá trị dương")

    must_positive_cols = [
        "Flow Duration",
        "Fwd Header Length",
        "Fwd Header Length.1",
        "Bwd Header Length",
        "min_seg_size_forward",
    ]
    must_positive_cols = [col for col in must_positive_cols if col in df.columns]
    negative_rows = ((df[must_positive_cols] < 0).any(axis=1)).sum()
    print(f"Số dòng chứa giá trị âm không hợp lệ: \n{negative_rows}")
    df = df[~(df[must_positive_cols] < 0).any(axis=1)]
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
    print(f"Các cột đã xóa: {constant_cols}")
    df = df.drop(columns=constant_cols)
    print(f"Số dòng, cột còn lại: {df.shape}")

    return df


# df_cleaned = data_cleaned(df)
