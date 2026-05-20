from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator

def run_isotonic_regression(raw_model, X_cal, y_cal, X_test):
    """
    Huấn luyện Isotonic Regression trên tập Calibration để hiệu chỉnh xác suất.
    
    Args:
        raw_model: Mô hình Logistic Regression đã được huấn luyện (từ baseline)
        X_cal, y_cal: Tập dữ liệu Calibration (20%)
        X_test: Tập dữ liệu Test để dự đoán (20%)
        
    Returns:
        iso_model: Mô hình đã được hiệu chỉnh
        y_prob_iso: Xác suất dự đoán sau hiệu chỉnh
        y_pred_iso: Nhãn dự đoán sau hiệu chỉnh
    """
    print("Đang huấn luyện mô hình Isotonic Regression trên tập Calibration...")
    frozen_model = FrozenEstimator(raw_model)
    
    # Khởi tạo Calibrator với estimator đã đóng băng
    iso_model = CalibratedClassifierCV(estimator=frozen_model, method='isotonic')
    
    # Huấn luyện bộ hiệu chỉnh (Calibrator) bằng tập Calibration
    iso_model.fit(X_cal, y_cal)
    
    # Lấy kết quả dự đoán trên tập Test
    y_pred_iso = iso_model.predict(X_test)
    y_prob_iso = iso_model.predict_proba(X_test)[:, 1]
    
    return iso_model, y_prob_iso, y_pred_iso
