# Hướng dẫn sử dụng Demo

## Tổng quan

Dự án này cung cấp 3 cách để dự đoán xem một network flow là **Benign** (bình thường) hay **Attack** (tấn công):

### 1. **demo.py** - Demo toàn bộ (Đầy đủ nhất)
- Cho phép nhập **toàn bộ 79 đặc trưng** của network flow
- Hoặc nhập từ file CSV
- Dự đoán và hiển thị xác suất

**Cách chạy:**
```bash
cd src
python -m modules.demo
```

**Cách sử dụng:**
```
1. Chọn "1" - Nhập thủ công từ bàn phím
   - Nhập các giá trị đặc trưng (hoặc bỏ qua = 0)
2. Hoặc chọn "2" - Nhập từ file CSV
   - Cung cấp đường dẫn file CSV
3. Xem kết quả dự đoán
```

**Ví dụ output:**
```
Phân loại: 🟢 BENIGN (Bình thường)

Xác suất dự đoán:
  - Benign:  0.9523 (95.23%)
  - Attack:  0.0477 (4.77%)
```

---

### 2. **demo_simple.py** - Demo với dữ liệu mẫu
- Tải dữ liệu từ `data/processed/tuesday_cleaned.csv`
- **Tự động test với 3 mẫu Benign + 3 mẫu Attack**
- Không cần nhập dữ liệu

**Cách chạy:**
```bash
cd src
python demo_simple.py
```

**Lưu ý:**
- Phải chạy `src/main.py` trước để xử lý dữ liệu
- Tạo file `data/processed/tuesday_cleaned.csv`

---

### 3. **demo_interactive.py** - Demo tương tác (Dễ sử dụng nhất)
- Giao diện đơn giản, dễ sử dụng
- 4 chế độ:
  1. **Nhập thủ công** - Chỉ nhập các đặc trưng chính (12 đặc trưng)
  2. **Demo nhanh** - Test với dữ liệu mẫu
  3. **Nhập từ CSV** - Tải flow từ file CSV
  4. **Thoát** - Kết thúc chương trình

**Cách chạy:**
```bash
cd src
python demo_interactive.py
```

**Các đặc trưng chính có thể nhập:**
```
1. Flow Duration - Độ dài luồng (ms)
2. Total Fwd Packets - Tổng gói dữ liệu phía trước
3. Total Backward Packets - Tổng gói dữ liệu phía sau
4. Total Length of Fwd Packets - Tổng độ dài gói phía trước (bytes)
5. Total Length of Bwd Packets - Tổng độ dài gói phía sau (bytes)
6. Flow Bytes/s - Số bytes mỗi giây
7. Flow Packets/s - Số gói mỗi giây
8. Fwd Packet Length Mean - Độ dài gói trung bình phía trước
9. Bwd Packet Length Mean - Độ dài gói trung bình phía sau
10. SYN Flag Count - Số flag SYN
11. FIN Flag Count - Số flag FIN
12. RST Flag Count - Số flag RST
```

---

## Chuẩn bị trước khi chạy

### Bước 1: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 2: Xử lý dữ liệu
```bash
chạy file main.py
```

Điều này sẽ:
- Làm sạch dữ liệu gốc từ `data/raw/Tuesday-WorkingHours.pcap_ISCX.csv`
- Lưu dữ liệu đã xử lý vào `data/processed/tuesday_cleaned.csv`
- Tạo mô hình huấn luyện Logistic Regression và 2 mô hình hiệu chỉnh Platt Scaling và Isotonic Regression
- Lưu mô hình vào `src/models/model.pkl`
- Lưu scaler vào `src/models/scaler.pkl`

### Bước 3: Chạy Demo
```bash
chạy file demo.py
```


### Mô hình: Logistic Regression
- **Input:** 79 đặc trưng network flow (sau khi chuẩn hóa)
- **Output:** Xác suất flow là Attack (0-1)
- **Phân loại:**
  - P < 0.5 → **BENIGN**
  - P ≥ 0.5 → **ATTACK**

### Dữ liệu huấn luyện
- **Source:** CICIDS2017 Dataset
- **Tập:** Tuesday-WorkingHours.pcap_ISCX.csv
- **Chia:**
  - Train: 60%
  - Calibration: 20%
  - Test: 20%


## Xử lý lỗi

### Lỗi: "Model chưa tồn tại"
**Giải pháp:** Chạy `src/main.py` trước để huấn luyện mô hình

### Lỗi: "File dữ liệu không tồn tại"
**Giải pháp:** Kiểm tra đường dẫn file CSV có chính xác không

### Lỗi: "Lỗi dự đoán"
**Giải pháp:** Đảm bảo dữ liệu nhập là số hợp lệ (không âm)

---

## Ghi chú kỹ thuật

### Quy trình tiền xử lý dữ liệu
1. **Làm sạch:** Loại bỏ NaN, Infinity, duplicate
2. **Encode:** Chuyển đổi cột phân loại thành số
3. **Chia tập:** Train 60%, Calibration 20%, Test 20%
4. **Chuẩn hóa:** Sử dụng StandardScaler

### Quy trình dự đoán
1. Tiếp nhận dữ liệu flow (dict hoặc DataFrame)
2. Xử lý tiền xử lý (chuẩn hóa, điền NaN)
3. Chuẩn hóa bằng scaler
4. Dự đoán bằng mô hình
5. Trả về nhãn (0=Benign, 1=Attack) và xác suất
