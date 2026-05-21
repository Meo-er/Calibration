import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    brier_score_loss,
)


def calculate_ece(y_true, y_prob, n_bins=10):
    """
    Hàm tính toán Expected Calibration Error (ECE).
    Chia dải xác suất [0, 1] thành n_bins, tính chênh lệch giữa
    độ chính xác thực tế (Accuracy) và độ tự tin (Confidence) ở mỗi bin.
    """
    # Đảm bảo y_true là numpy array để dễ dùng boolean mask
    y_true = np.array(y_true)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        # Tìm các mẫu có xác suất rơi vào bin hiện tại
        if i == n_bins - 1:
            bin_mask = (y_prob >= bin_edges[i]) & (y_prob <= bin_edges[i + 1])
        else:
            bin_mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])

        n_samples = np.sum(bin_mask)

        if n_samples > 0:
            # Độ chính xác thực tế của bin (Accuracy)
            true_acc = np.mean(y_true[bin_mask])
            # Xác suất dự đoán trung bình của bin (Confidence)
            pred_conf = np.mean(y_prob[bin_mask])

            # Trọng số của bin (dựa trên số lượng mẫu)
            weight = n_samples / len(y_prob)

            # Cộng dồn vào ECE
            ece += weight * np.abs(true_acc - pred_conf)

    return ece


def run_baseline(X_train, X_test, y_train):
    # print("HUẤN LUYỆN VÀ ĐÁNH GIÁ BASELINE")
    # print("-" * 40)

    # 1. Khởi tạo mô hình Logistic Regression
    # Dùng class_weight="balanced" để xử lý mất cân bằng dữ liệu
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")

    # 2. Huấn luyện mô hình
    print("Đang huấn luyện mô hình Logistic Regression...")
    model.fit(X_train, y_train)

    # 3. Dự đoán trên tập test
    y_pred = model.predict(X_test)  # Nhãn cứng (0 hoặc 1)
    y_prob = model.predict_proba(X_test)[:, 1]  # Xác suất rơi vào lớp 1 (Attack)

    # 4. Tính toán các Metric
    # cm = confusion_matrix(y_test, y_pred)
    # tn, fp, fn, tp = cm.ravel()

    # # False Positive Rate (Tỷ lệ báo động nhầm)
    # fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

    # acc = accuracy_score(y_test, y_pred)
    # prec = precision_score(y_test, y_pred, zero_division=0)
    # rec = recall_score(y_test, y_pred, zero_division=0)
    # f1 = f1_score(y_test, y_pred, zero_division=0)

    # Tính Brier Score và ECE
    # brier = brier_score_loss(y_test, y_prob)
    # ece = calculate_ece(y_test, y_prob, n_bins=10)

    # 5. In kết quả
    # print("\nKẾT QUẢ ĐÁNH GIÁ TRÊN TẬP TEST (20%):")
    # print(f"Accuracy           : {acc:.4f}")
    # print(f"Precision          : {prec:.4f}")
    # print(f"Recall             : {rec:.4f}  <-- Quan trọng cho IDS")
    # print(f"F1-Score           : {f1:.4f}  <-- Thước đo cân bằng")
    # print(f"FPR (Báo giả)      : {fpr:.4f}  <-- Càng thấp càng tốt")
    # print(f"Brier Score        : {brier:.4f}  <-- Metric cốt lõi cho Calibration")
    # print(f"ECE                : {ece:.4f}  <-- Mức độ chênh lệch xác suất trung bình")

    # print("\nConfusion Matrix:")
    # print(f"TN: {tn} | FP: {fp}")
    # print(f"FN: {fn} | TP: {tp}")
    # print("-" * 40)

    return model, y_prob, y_pred
