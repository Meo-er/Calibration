import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.calibration import calibration_curve

# Thư mục mặc định để lưu ảnh
SAVE_DIR = "./results"
os.makedirs(SAVE_DIR, exist_ok=True)

# Vẽ phân bố nhãn
def plot_label_distribution(y, next_plot=True):
    label_counts = y.value_counts()
    plt.figure(figsize=(6, 4))
    sns.barplot(x=label_counts.index, y=label_counts.values)
    plt.xticks(ticks=[0, 1], labels=["Benign (0)", "Attack (1)"])
    plt.ylabel("Số lượng mẫu")
    plt.title("Phân bố nhãn Benign vs Attack")

    save_path = os.path.join(SAVE_DIR, "label_distribution.png")
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    print(f"[*] Đã lưu biểu đồ tại: {save_path}")

    plt.show(block=False)
    plt.pause(1)
    if next_plot:
        input("\nNhấn Enter để xem biểu đồ tiếp theo")
        plt.close()


# Vẽ boxplot cho một số đặc trưng quan tâm
def plot_feature_boxplot(df, features, next_plot=True):
    fig, axes = plt.subplots(1, len(features), figsize=(15, 4))

    # Nếu chỉ có 1 đặc trưng, axes không phải là list
    if len(features) == 1:
        axes = [axes]

    for i, feat in enumerate(features):
        if feat in df.columns:
            # Lấy dữ liệu của đặc trưng (bỏ qua NaN)
            data = df[feat].dropna()

            # Tính các chỉ số thống kê
            min_val = data.min()
            max_val = data.max()
            q1 = data.quantile(0.25)
            median = data.median()
            q3 = data.quantile(0.75)
            iqr = q3 - q1

            # Tính outlier (giá trị nằm ngoài 1.5*IQR)
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_count = ((data < lower_bound) | (data > upper_bound)).sum()
            outlier_percent = outlier_count / len(data) * 100

            # In chi tiết thống kê
            print(f"\nTHỐNG KÊ CHI TIẾT CHO ĐẶC TRƯNG: {feat}")
            print("=" * 50)
            print(f"  Số lượng mẫu (sau xử lý): {len(data):,}")
            print(f"  Giá trị nhỏ nhất (Min):   {min_val:.4f}")
            print(f"  Giá trị lớn nhất (Max):   {max_val:.4f}")
            print(f"  Trung vị (Median - Q2):   {median:.4f}")
            print(f"  Tứ phân vị thứ nhất (Q1): {q1:.4f}")
            print(f"  Tứ phân vị thứ ba (Q3):   {q3:.4f}")
            print(f"  Khoảng tứ phân vị (IQR):  {iqr:.4f}")
            print(
                f"  Số lượng outlier:         {outlier_count} ({outlier_percent:.2f}%)"
            )
            print(
                f"  Giá trị outlier cao nhất: {data[data > upper_bound].max() if outlier_count > 0 else 'không có'}"
            )

            # Vẽ boxplot
            sns.boxplot(data=df, y=feat, ax=axes[i])
            axes[i].set_ylabel(feat)
            axes[i].set_title(f"Boxplot của {feat}")

    plt.tight_layout()

    save_path = os.path.join(SAVE_DIR, "feature_boxplot.png")
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    print(f"\n[*] Đã lưu biểu đồ tại: {save_path}")

    plt.show(block=False)
    plt.pause(1)
    if next_plot:
        input("\nNhấn Enter để xem biểu đồ tiếp theo")
        plt.close()


# Vẽ Confusion Matrix
def plot_confusion_matrix(y_test, y_pred, next_plot=True):
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["Benign", "Attack"]
    )
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix - Logistic Regression (Raw)")

    save_path = os.path.join(SAVE_DIR, "confusion_matrix.png")
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    print(f"\n[*] Đã lưu biểu đồ tại: {save_path}")


    tn, fp, fn, tp = cm.ravel()
    print("\nCONFUSION MATRIX")
    print(f"True Negative (Benign đúng):   {tn}")
    print(f"False Positive (Cảnh báo sai): {fp}")
    print(f"False Negative (Bỏ sót):       {fn}")
    print(f"True Positive (Phát hiện đúng): {tp}")
    print()
    print(f"Tỷ lệ False Alarm (FP/Benign): {fp/(tn+fp)*100:.2f}%")
    print(f"Tỷ lệ bỏ sót (FN/Attack):     {fn/(fn+tp)*100:.2f}%")
    print()
    
    plt.show(block=False)
    plt.pause(1)
    if next_plot:
        input("\nNhấn Enter để xem biểu đồ tiếp theo")
        plt.close()


# Vẽ Reliability Diagram (Calibration Curve)
def plot_reliability_diagram(y_test, y_pred_prob, next_plot=True):
    prob_true, prob_pred = calibration_curve(y_test, y_pred_prob, n_bins=10)

    plt.figure(figsize=(6, 6))
    plt.plot(
        prob_pred, prob_true, marker="o", linewidth=2, label="Logistic Regression (Raw)"
    )
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfect Calibration")
    plt.xlabel("Mean Predicted Probability")
    plt.ylabel("Fraction of Positives (Actual Probability)")
    plt.title("Reliability Diagram - Raw Model (Before Calibration)")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(SAVE_DIR, "reliability_diagram.png")
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    print(f"[*] Đã lưu biểu đồ tại: {save_path}")

    print("\nRELIABILITY DIAGRAM - CHI TIẾT CÁC BIN")
    print(f"{'Bin':<6} {'Dự đoán TB':<12} {'Thực tế':<10} {'Chênh lệch':<10}")
    print("-" * 45)
    for i, (p_pred, p_true) in enumerate(zip(prob_pred, prob_true)):
        diff = p_pred - p_true
        print(f"Bin {i+1:<2}  {p_pred:.4f}      {p_true:.4f}     {diff:+.4f}")
    print()

    plt.show(block=False)
    plt.pause(1)
    if next_plot:
        input("\nNhấn Enter để kết thúc")
        plt.close()
