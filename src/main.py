import pandas as pd

from modules.overview import data_overview
from modules.cleaning import data_cleaned
from modules.preprocessing import preprocess_baseline
from modules.baseline import run_baseline
from modules.evaluation import (
    plot_label_distribution,
    plot_confusion_matrix,
    plot_reliability_diagram,
    plot_feature_boxplot,
)

# Read
readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
df = pd.read_csv(readFile)

# Overview
data_overview(df)
df_cleaned = data_cleaned(df)
df_cleaned.to_csv("./data/processed/tuesday_cleaned.csv", index=False)

# Chia dữ liệu
X_train, X_cal, X_test, y_train, y_cal, y_test, scaler = preprocess_baseline(df_cleaned)

# Biểu đồ dữ liệu ban đầu
y_total = pd.concat([y_train, y_cal, y_test])
print("\nPHÂN BỐ NHÃN BAN ĐẦU")
print(f"Tổng số mẫu: {len(y_total)}")
print(f"Số Benign: {(y_total == 0).sum()}")
print(f"Số Attack: {(y_total == 1).sum()}")
plot_label_distribution(y_total)

# phân tích 3 đặc trưng
feature_sample = ["Flow Duration", "Total Fwd Packets", "Flow Bytes/s"]
existing_features = [f for f in feature_sample if f in df_cleaned.columns]
if existing_features:
    plot_feature_boxplot(df_cleaned, existing_features)
# Baseline
model, y_prob = run_baseline(X_train, X_test, y_train, y_test)
y_pred = model.predict(X_test)

# Biểu đồ baseline
plot_confusion_matrix(y_test, y_pred)

plot_reliability_diagram(y_test, y_prob)
