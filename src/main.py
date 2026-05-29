import pandas as pd
import joblib
import os

from modules.overview import data_overview
from modules.cleaning import data_cleaned
from modules.preprocess_train import preprocess_train
from modules.baseline import run_baseline
from modules.evaluation import (
    plot_label_distribution,
    plot_confusion_matrix,
    plot_reliability_diagram,
    plot_feature_boxplot,
    evaluation_model,
    print_performance_comparison_table,
)
from modules.Calibration.platt_scaling import platt_scaling
from modules.Calibration.isotonic_regression import run_isotonic_regression
from modules.analysis import extract_and_analyze_errors

# Tạo thư mục models nếu chưa tồn tại
models_dir = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(models_dir, exist_ok=True)

# Read
readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
df = pd.read_csv(readFile)

# Overview

data_overview(df)
df_cleaned = data_cleaned(df)
benign = (df_cleaned["Label"] == "BENIGN").sum()
attack = (df_cleaned["Label"] != "BENIGN").sum()
total = len(df_cleaned)
benign_percent = (benign / total) * 100
attack_percent = (attack / total) * 100
print(f"Tỷ lệ Benign:Attack = {benign}:{attack} ~ {benign/attack:.0f}:1")
print(f"Tỷ lệ phần trăm:")
print(f"  - Benign: {benign_percent:.2f}%")
print(f"  - Attack: {attack_percent:.2f}%")

df_cleaned.to_csv("./data/processed/tuesday_cleaned.csv", index=False)

# Chia dữ liệu
(
    X_train,
    X_cal,
    X_test,
    X_test_raw,
    y_train,
    y_cal,
    y_test,
    scaler,
    encoders,
    feature_columns,
) = preprocess_train(df_cleaned)

# Lưu tập test để chạy demo
test_df = pd.DataFrame(X_test_raw, columns=feature_columns)
test_df["Label"] = y_test.map({0: "BENIGN", 1: "ATTACK"})

test_df.to_csv("./data/processed/test_set.csv", index=False)

print("Đã lưu test_set.csv")
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


# Save model
joblib.dump(platt_model, os.path.join(models_dir, "model_platt.pkl"))
joblib.dump(iso_model, os.path.join(models_dir, "model_iso.pkl"))
joblib.dump(model, os.path.join(models_dir, "model_baseline.pkl"))

# Save scaler
joblib.dump(scaler, os.path.join(models_dir, "scaler.pkl"))

# Save encoders
joblib.dump(encoders, os.path.join(models_dir, "encoders.pkl"))

# Save feature columns
joblib.dump(feature_columns, os.path.join(models_dir, "features.pkl"))

print("Đã lưu model!")

# Metrics
metrics_base = evaluation_model(
    y_test, y_pred, y_prob, model_name="Logistic Regression (Raw)"
)

metrics_platt = evaluation_model(
    y_test, y_pred_platt, y_prob_platt, model_name="Platt Scaling"
)

metrics_iso = evaluation_model(
    y_test, iso_pred, iso_prob, model_name="Isotonic Regression"
)

# Biểu đồ baseline
plot_confusion_matrix(y_test, y_pred, model_name="Logistic Regression (Raw)")
plot_reliability_diagram(y_test, y_prob, model_name="Logistic Regression (Raw)")

plot_confusion_matrix(y_test, y_pred_platt, model_name="Platt Scaling")
plot_reliability_diagram(y_test, y_prob_platt, model_name="Platt Scaling")

plot_confusion_matrix(y_test, iso_pred, model_name="Isotonic Regression")
plot_reliability_diagram(y_test, iso_prob, model_name="Isotonic Regression")

# Bảng so sánh hiệu năng giữa các mô hình
print_performance_comparison_table(metrics_base, metrics_platt, metrics_iso)

# Tự động quét tập Test thực tế để trích xuất và phân tích 5 mẫu lỗi hành vi mạng
extract_and_analyze_errors(y_test.values, y_prob, y_prob_platt, iso_prob)
