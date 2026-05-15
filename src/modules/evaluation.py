import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.calibration import calibration_curve


# Vẽ phân bố nhãn
def plot_label_distribution(y, next_plot=True):
    label_counts = y.value_counts()
    plt.figure(figsize=(6, 4))
    sns.barplot(x=label_counts.index, y=label_counts.values)
    plt.xticks(ticks=[0, 1], labels=["Benign (0)", "Attack (1)"])
    plt.ylabel("Số lượng mẫu")
    plt.title("Phân bố nhãn Benign vs Attack")
    plt.show(block=False)
    plt.pause(1)
    if next_plot:
        input("\nNhấn Enter để xem biểu đồ tiếp theo")
        plt.close()


# Vẽ boxplot cho một số đặc trưng quan tâm
def plot_feature_boxplot(df, features, next_plot=True):
    fig, axes = plt.subplots(1, len(features), figsize=(15, 4))
    for i, feat in enumerate(features):
        if feat in df.columns:
            sns.boxplot(data=df, y=feat, ax=axes[i])
            axes[i].set_title(f"Boxplot của {feat}")
    plt.tight_layout()
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
    plt.show(block=False)
    plt.pause(1)

    tn, fp, fn, tp = cm.ravel()
    print("CONFUSION MATRIX")
    print(f"True Negative (Benign đúng):   {tn}")
    print(f"False Positive (Cảnh báo sai): {fp}")
    print(f"False Negative (Bỏ sót):       {fn}")
    print(f"True Positive (Phát hiện đúng): {tp}")
    print()
    print(f"Tỷ lệ False Alarm (FP/Benign): {fp/(tn+fp)*100:.2f}%")
    print(f"Tỷ lệ bỏ sót (FN/Attack):     {fn/(fn+tp)*100:.2f}%")
    print()

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
    plt.show(block=False)
    plt.pause(1)

    print("RELIABILITY DIAGRAM - CHI TIẾT CÁC BIN")
    print(f"{'Bin':<6} {'Dự đoán TB':<12} {'Thực tế':<10} {'Chênh lệch':<10}")
    print("-" * 45)
    for i, (p_pred, p_true) in enumerate(zip(prob_pred, prob_true)):
        diff = p_pred - p_true
        print(f"Bin {i+1:<2}  {p_pred:.4f}      {p_true:.4f}     {diff:+.4f}")
    print()

    if next_plot:
        input("\nNhấn Enter để kết thúc")
        plt.close()
