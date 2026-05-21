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
    evaluation_model,
)
from modules.Calibration.platt_scaling import platt_scaling
from modules.Calibration.isotonic_regression import run_isotonic_regression

# Read
readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
df = pd.read_csv(readFile)

# Overview

data_overview(df)
df_cleaned = data_cleaned(df)
benign = (df_cleaned["Label"] == "BENIGN").sum()
attack = (df_cleaned["Label"] != "BENIGN").sum()
print(f"Tỷ lệ Benign:Attack = {benign}:{attack} ~ {benign/attack:.0f}:1")

df_cleaned.to_csv("./data/processed/tuesday_cleaned.csv", index=False)

# Chia dữ liệu
X_train, X_cal, X_test, y_train, y_cal, y_test = preprocess_baseline(df_cleaned)

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
model, y_prob, y_pred = run_baseline(X_train, X_test, y_train)
# Platt Scaling
platt_model, y_prob_platt, y_pred_platt = platt_scaling(model, X_cal, y_cal, X_test)
# Isotonic Regression
iso_model, iso_prob, iso_pred = run_isotonic_regression(model, X_cal, y_cal, X_test)

# Metrics
evaluation_model(y_test, y_pred, y_prob, model_name="Logistic Regression (Raw)")
evaluation_model(y_test, y_pred_platt, y_prob_platt, model_name="Platt Scaling")

# Biểu đồ baseline
plot_confusion_matrix(y_test, y_pred, model_name="Logistic Regression (Raw)")
plot_reliability_diagram(y_test, y_prob, model_name="Logistic Regression (Raw)")

plot_confusion_matrix(y_test, y_pred_platt, model_name="Platt Scaling")
plot_reliability_diagram(y_test, y_prob_platt, model_name="Platt Scaling")

plot_confusion_matrix(y_test, iso_pred, model_name="Isotonic Regression")
plot_reliability_diagram(y_test, iso_prob, model_name="Isotonic Regression")
