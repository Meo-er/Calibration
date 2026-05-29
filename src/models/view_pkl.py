# file này để xem pkl nếu cần thôi

import os
import joblib

# 1. Lấy đường dẫn đến chính thư mục chứa file view_pkl.py hiện tại (tức là thư mục models)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Tạo đường dẫn tuyệt đối chính xác đến file model.pkl nằm cùng thư mục
model_path = os.path.join(current_dir, "model_iso.pkl")

# Đọc file bằng đường dẫn tuyệt đối vừa tạo
obj = joblib.load(model_path)

# Xem kiểu dữ liệu
print("Kiểu dữ liệu của encoders:", type(obj))

# In nội dung
print("Nội dung encoders:")
print(obj)
