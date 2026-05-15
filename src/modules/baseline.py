import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
<<<<<<< HEAD
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    brier_score_loss,
)


def run_baseline(X_train, X_test, y_train, y_test):
    print("\nHUẤN LUYỆN VÀ ĐÁNH GIÁ BASELINE")
    print("-" * 40)

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
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    # False Positive Rate (Tỷ lệ báo động nhầm)
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

=======
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, brier_score_loss
)

def run_baseline(X_train, X_test, y_train, y_test):
    print("HUẤN LUYỆN VÀ ĐÁNH GIÁ BASELINE")
    print("-" * 40)
    
    # 1. Khởi tạo mô hình Logistic Regression
    # Dùng class_weight="balanced" để xử lý mất cân bằng dữ liệu
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    
    # 2. Huấn luyện mô hình
    print("Đang huấn luyện mô hình Logistic Regression...")
    model.fit(X_train, y_train)
    
    # 3. Dự đoán trên tập test
    y_pred = model.predict(X_test)               # Nhãn cứng (0 hoặc 1)
    y_prob = model.predict_proba(X_test)[:, 1]   # Xác suất rơi vào lớp 1 (Attack)
    
    # 4. Tính toán các Metric
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # False Positive Rate (Tỷ lệ báo động nhầm)
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    
>>>>>>> fca8a80da6cbc6296721ad48f1e6d3051519041d
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    brier = brier_score_loss(y_test, y_prob)
<<<<<<< HEAD

=======
    
>>>>>>> fca8a80da6cbc6296721ad48f1e6d3051519041d
    # 5. In kết quả
    print("\nKẾT QUẢ ĐÁNH GIÁ TRÊN TẬP TEST (20%):")
    print(f"Accuracy           : {acc:.4f}")
    print(f"Precision          : {prec:.4f}")
    print(f"Recall             : {rec:.4f}  <-- Quan trọng cho IDS")
    print(f"F1-Score           : {f1:.4f}  <-- Thước đo cân bằng")
    print(f"FPR (Báo giả)      : {fpr:.4f}  <-- Càng thấp càng tốt")
    print(f"Brier Score        : {brier:.4f}  <-- Metric cốt lõi cho Calibration")
<<<<<<< HEAD

=======
    
>>>>>>> fca8a80da6cbc6296721ad48f1e6d3051519041d
    print("\nConfusion Matrix:")
    print(f"TN: {tn} | FP: {fp}")
    print(f"FN: {fn} | TP: {tp}")
    print("-" * 40)
<<<<<<< HEAD

=======
    
>>>>>>> fca8a80da6cbc6296721ad48f1e6d3051519041d
    return model, y_prob
