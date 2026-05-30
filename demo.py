import pandas as pd
import os
import sys
import joblib


from src.predict import predict_flow

# Load feature columns for validation
models_dir = os.path.join(os.path.dirname(__file__), "src", "models")
try:
    feature_columns = joblib.load(os.path.join(models_dir, "features.pkl"))
except:
    feature_columns = None
    print("⚠️  Warning: Could not load feature_columns")

print("\nĐang đọc dữ liệu từ file test_set.csv...")

try:
    df_data = pd.read_csv("data/processed/test_set.csv")
    print(f"Dữ liệu đã đọc: {df_data.shape[0]:,} dòng")
except FileNotFoundError:
    print(
        "Dữ liệu không tìm thấy. Vui lòng chạy 'python src/main.py' trước để tạo dữ liệu đã xử lý."
    )
    sys.exit(1)


def display_result(results, truth=None):

    if truth:
        print(f"Nhãn đúng: {truth}")

    for method, result in results.items():

        # 1. Lấy xác suất dự đoán (prob) từ kết quả
        prob = result["prob"]
        
        # 2. Phân nhánh ngưỡng cắt tối ưu cho từng mô hình theo báo cáo tuần 4
        if "Isotonic" in method:
            threshold = 0.35
        elif "Platt" in method:
            threshold = 0.42
        else: # Dành cho mô hình Raw Logistic Regression
            threshold = 0.50
            
        # 3. Ép lại nhãn phân loại dựa trên ngưỡng tối ưu mới
        if prob >= threshold:
            label = "ATTACK"
        else:
            label = "BENIGN"

        print("\n" + "-" * 60)
        print(f"Mô hình: {method}")
        print(f"Ngưỡng cắt (Threshold) đang dùng: {threshold}")

        print(f"Prediction: {label}")
        print(f"Probability : {prob:.6f}")

        print(f"\nBENIGN : {(1 - prob)*100:.2f}%")
        print(f"ATTACK : {prob*100:.2f}%")


def mode_predict_file():
    predict_sample = pd.read_csv("data_sample/data_sample.csv")
    predict_sample.columns = predict_sample.columns.str.strip()

    print(f"\nĐã đọc {len(predict_sample)} dòng")

    for idx, row in predict_sample.iterrows():
        truth = row.get("Label", "None")
        flow = row.drop("Label", errors="ignore").to_dict()

        cleaned_flow = {}
        for key, val in flow.items():
            clean_key = str(key).strip()
            cleaned_flow[clean_key] = val
        print("\n=====")
        print(f"Flow #{idx + 1}:")
        # print(f"  Labels đúng: {truth}")
        # print(f"  Số cột input: {len(cleaned_flow)}")
        # print(f"  Số cột expected: {len(feature_columns)}")

        # ✓ QUAN TRỌNG: So sánh sample giá trị
        # if idx == 0:
        #     print("\n  --- DEBUG: So sánh 5 giá trị đầu ---")
        #     for key in list(cleaned_flow.keys())[:5]:
        #         val = cleaned_flow[key]
        #         print(f"    {key}: {val} (type: {type(val).__name__})")

        #     # Lấy 1 dòng từ df_data để so sánh
        #     sample_from_df = df_data.iloc[0].drop("Label").to_dict()
        #     print("\n  --- Từ df_data (mode 2/3) ---")
        #     for key in list(sample_from_df.keys())[:5]:
        #         val = sample_from_df[key]
        #         print(f"    {key}: {val} (type: {type(val).__name__})")

        # missing_cols = set(feature_columns) - set(cleaned_flow.keys())
        # if missing_cols:
        #     print(f"  ⚠️  Missing columns: {missing_cols}")
        # if idx == 0:

        #     original_row = df_data.iloc[0].drop("Label")
        #     sample_row = pd.Series(cleaned_flow)

        # print("\n===== DEBUG FULL COMPARE =====")

        # for col in feature_columns:

        #     val1 = original_row[col]
        #     val2 = sample_row[col]

        #     if str(val1) != str(val2):

        #         print(f"\nCOLUMN: {col}")
        #         print(f"df_data : {val1} ({type(val1).__name__})")
        #         print(f"sample  : {val2} ({type(val2).__name__})")

        results = predict_flow(cleaned_flow)
        display_result(results, truth=truth)


def mode_benign():

    benign_samples = df_data[df_data["Label"] == "BENIGN"]

    # DEBUG
    # sampled_row = benign_samples.sample(1)
    # print(f"\nDEBUG: Index được chọn = {sampled_row.index[0]}")

    sample = benign_samples.sample(1).iloc[0]
    # print(sample)
    flow = sample.drop("Label").to_dict()

    results = predict_flow(flow)

    display_result(results, truth="BENIGN")


def mode_attack():

    attack_samples = df_data[df_data["Label"] != "BENIGN"]

    sample = attack_samples.sample(1).iloc[0]
    # print(sample)

    flow = sample.drop("Label").to_dict()

    results = predict_flow(flow)

    display_result(results, truth="ATTACK")


def show_menu():

    print("\n" + "=" * 60)
    print("1. Test file data_sample.csv")
    print("2. Test BENIGN sample")
    print("3. Test ATTACK sample")
    print("0. Thoát")

    print("=" * 60)

    return input("\nLựa chọn: ")


def main():

    while True:

        choice = show_menu()

        if choice == "1":

            mode_predict_file()

        elif choice == "2":

            mode_benign()

        elif choice == "3":

            mode_attack()

        elif choice == "0":

            print("\nHoàn tất demo.")
            break

        else:

            print("Lựa chọn không hợp lệ!")


# =====================================================================
if __name__ == "__main__":
    main()
