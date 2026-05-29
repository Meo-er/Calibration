import os
import pandas as pd
import numpy as np


def extract_and_analyze_errors(y_true, y_prob_raw, y_prob_platt, y_prob_iso):
    """
    Hàm tự động trích xuất và phân tích lỗi từ dữ liệu chạy thực tế
    """
    print("PHÂN HỆ TỰ ĐỘNG TRÍCH XUẤT VÀ PHÂN TÍCH LỖI DÒNG DỮ LIỆU THỰC TẾ")

    threshold = 0.5
    y_pred_raw = (y_prob_raw >= threshold).astype(int)
    y_pred_platt = (y_prob_platt >= threshold).astype(int)
    y_pred_iso = (y_prob_iso >= threshold).astype(int)

    # 1. Tìm các ca lỗi bằng logic NumPy
    fp_all = np.where(
        (y_true == 0) & (y_pred_raw == 1) & (y_pred_platt == 1) & (y_pred_iso == 1)
    )[0]
    fixed_success = np.where((y_true == 0) & (y_pred_raw == 1) & (y_pred_iso == 0))[0]
    fn_tradeoff = np.where((y_true == 1) & (y_pred_raw == 1) & (y_pred_iso == 0))[0]

    selected_indices = []
    error_behaviors = {}

    if len(fp_all) >= 2:
        # Bốc ngẫu nhiên 2 mẫu không trùng nhau (replace=False) từ danh sách lỗi FP
        chosen_fp = np.random.choice(fp_all, size=2, replace=False)
        selected_indices.extend(chosen_fp)
        error_behaviors[chosen_fp[0]] = (
            "False Positive (Báo giả): Gói tin thường mang thuộc tính bất thường đánh lừa cả mô hình thô lẫn phân hệ hiệu chuẩn."
        )
        error_behaviors[chosen_fp[1]] = (
            "False Positive (Báo giả): Cả 3 cấu hình đều sai do gói tin mang đặc trưng nhiễu mạnh, gây hiểu nhầm hệ thống."
        )
    elif len(fp_all) == 1:
        selected_indices.append(fp_all[0])
        error_behaviors[fp_all[0]] = (
            "False Positive (Báo giả): Cả 3 cấu hình đều sai do gói tin mang đặc trưng nhiễu mạnh."
        )

    if len(fixed_success) >= 2:
        # Bốc ngẫu nhiên 2 mẫu không trùng nhau từ danh sách sửa lỗi thành công
        chosen_fixed = np.random.choice(fixed_success, size=2, replace=False)
        selected_indices.extend(chosen_fixed)
        error_behaviors[chosen_fixed[0]] = (
            "Sửa lỗi thành công: Mô hình Baseline thô gán nhầm vùng biên, thuật toán hiệu chuẩn kéo sụt xác suất về đúng nhãn BENIGN."
        )
        error_behaviors[chosen_fixed[1]] = (
            "Sửa lỗi thành công: Triệt tiêu cảnh báo giả vùng biên nhạy cảm nhờ năng lực nắn mịn phân phối dải xác suất đầu ra."
        )
    elif len(fixed_success) == 1:
        selected_indices.append(fixed_success[0])
        error_behaviors[fixed_success[0]] = (
            "Sửa lỗi thành công: Mô hình thô gán nhầm vùng biên, thuật toán hiệu chuẩn kéo sụt xác suất về đúng."
        )

    if len(fn_tradeoff) >= 1:
        # Bốc ngẫu nhiên 1 mẫu duy nhất từ danh sách bỏ sót
        chosen_fn = np.random.choice(fn_tradeoff, size=1)[0]
        selected_indices.append(chosen_fn)
        error_behaviors[
            chosen_fn[0] if isinstance(chosen_fn, np.ndarray) else chosen_fn
        ] = "False Negative (Bỏ sót): Mô hình thô bắt trúng ở mức ranh giới, tuy nhiên bộ hiệu chuẩn làm mịn xác suất vô tình đẩy giá trị xuống dưới mốc 0.5 gây lọt lưới."

    # Loại bỏ trùng lặp nếu có và sắp xếp lại thứ tự index tăng dần cho đẹp bảng
    selected_indices = sorted(list(set(selected_indices)))
    analysis_rows = []

    for idx in selected_indices:
        real_y = y_true[idx]
        analysis_rows.append(
            {
                "Index mẫu (Thật)": idx,
                "Nhãn đúng": "ATTACK (1)" if real_y == 1 else "BENIGN (0)",
                "Xác suất Raw": f"{y_prob_raw[idx]*100:.2f}%",
                "Dự đoán Raw": y_pred_raw[idx],
                "Xác suất Platt": f"{y_prob_platt[idx]*100:.2f}%",
                "Dự đoán Platt": y_pred_platt[idx],
                "Xác suất Isotonic": f"{y_prob_iso[idx]*100:.2f}%",
                "Dự đoán Isotonic": y_pred_iso[idx],
                "Bản chất lỗi hệ thống / Hành vi dòng lưu lượng mạng": error_behaviors.get(
                    idx, "Mẫu phân tích lỗi hệ thống."
                ),
            }
        )

    df_analysis = pd.DataFrame(analysis_rows)

    if not df_analysis.empty:
        import textwrap
        from tabulate import tabulate

        # Tự động xuống dòng gọn gàng cho cột giải thích dài
        df_analysis["Bản chất lỗi hệ thống / Hành vi dòng lưu lượng mạng"] = (
            df_analysis["Bản chất lỗi hệ thống / Hành vi dòng lưu lượng mạng"].apply(
                lambda x: "\n".join(textwrap.wrap(x, width=45))
            )
        )

        # Đổi tên cột ngắn lại một chút để bảng không bị quá bè ngang
        df_analysis.columns = [
            "Index",
            "Nhãn đúng",
            "Xác suất Raw",
            "Dự đoán\nRaw",
            "Xác suất Platt",
            "Dự đoán\nPlatt",
            "Xác suất Isotonic",
            "Dự đoán\nIso",
            "Bản chất lỗi hệ thống / Hành vi dòng lưu lượng mạng",
        ]

        # Sử dụng format 'grid' để vẽ khung lưới bao quanh từng ô cực kỳ ngay ngắn
        print(tabulate(df_analysis, headers="keys", tablefmt="grid", showindex=False))
    else:
        print("[!] Không tìm thấy mẫu dữ liệu nào thoả mãn các bộ điều kiện lọc lỗi.")


def main():
    print(f"\n{'PHÂN HỆ KHẢO SÁT VÀ PHÂN TÍCH LỖI CHUYÊN SÂU':^147}")

    path_to_csv = "./results/test_predictions.csv"

    # Kiểm tra xem file CSV đã tồn tại chưa
    if not os.path.exists(path_to_csv):
        print(f"[!] LỖI: Không tìm thấy file dữ liệu thực nghiệm tại: {path_to_csv}")
        print("[!] Vui lòng chạy file pipeline chính để xuất dữ liệu trước.")
        return

    print(f"[*] Đang đọc dữ liệu từ: {path_to_csv}")
    df_test = pd.read_csv(path_to_csv)

    # Đọc mảng giá trị từ file CSV
    y_true = df_test["y_true"].values
    y_prob_raw = df_test["prob_raw"].values
    y_prob_platt = df_test["prob_platt"].values
    y_prob_iso = df_test["prob_iso"].values

    # Chạy phân tích lỗi
    extract_and_analyze_errors(y_true, y_prob_raw, y_prob_platt, y_prob_iso)


if __name__ == "__main__":
    main()
