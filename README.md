# Đề tài: 29 - Hiệu chỉnh xác suất dự đoán cho IDS nhị phân trên bộ dữ liệu CICIDS2017
## 📌 Tổng quan đề tài
Dự án tập trung vào việc xây dựng hệ thống phát hiện xâm nhập mạng (IDS) phân loại nhị phân (**BENIGN** - Bình thường và **ATTACK** - Tấn công) sử dụng thuật toán **Logistic Regression** trên bộ dữ liệu chuẩn **CICIDS2017**.

Do các mô hình phân loại truyền thống thường đưa ra mức độ tự tin (xác suất) bị sai lệch so với tần suất thực tế, dự án này áp dụng hai phương pháp hiệu chỉnh xác suất nổi tiếng:
* **Platt Scaling (Sigmoid Method):** Phù hợp với các tập dữ liệu nhỏ hoặc mô hình bị lệch tuyến tính.
* **Isotonic Regression:** Phương pháp phi tham số mạnh mẽ, tự do uốn nắn đường cong xác suất khi có đủ dữ liệu.

**Mục tiêu:** Đưa xác suất dự đoán của IDS về gần với xác suất thực tế nhất, giúp giảm tỷ lệ cảnh báo sai (False Positive) trong giám sát an ninh mạng.
## Hướng dẫn cài đặt

1. Clone dự án: `git clone [LINK_DỰ_ÁN]`
2. Cài đặt các Extension cần thiết (Khuyến nghị VSCode): Black Formatter, Jupyter, Pylance
3. Kích hoạt môi trường ảo: `.\venv\Scripts\activate`
4. Cài thư viện: `pip install -r requirements.txt`

## Dữ liệu sử dụng (Dataset)
* **Bộ dữ liệu gốc:** [CICIDS2017 Dataset](https://www.unb.ca/cic/datasets/ids-2017.html) được cung cấp bởi Viện An ninh mạng Canada (CIC).
* **Phạm vi thực hiện:** Dự án sử dụng file Tuesday-WorkingHours`.csv`, được chuyển hóa về dạng nhị phân gồm Benign (0) và Attack (1). 
* **Lưu ý cài đặt:** Do dung lượng tập dữ liệu gốc lớn, thành viên nhóm hoặc người kiểm thử cần tải file dữ liệu từ nguồn trên, giải nén và đặt vào thư mục `data/raw/` trước khi tiến hành chạy pipeline huấn luyện.

## Cấu trúc thư mục

```
Calibration/
├── data/
│ ├── raw/                  #Lưu dữ liệu gốc
│ └── processed/            #Lưu dữ liệu đã xử lý
├── notebooks/              #Lưu notebook thử nghiệm
├── src/                    #Lưu code xử lý chính
│   ├── modules/            #Các hàm/module 
│   ├── models/             #Lưu trữ mô hình (.pkl) và các bộ tiền xử lý
│   ├── predict.py          #Thực hiện dự đoán 
│   └── main.py             #Luồng chạy chính của dự án
├── report/                 #Lưu báo cáo
├── demo.py                 #Demo dự án
├── results/                #Lưu bảng kết quả và biểu đồ
└── requirements.txt        #Ghi các thư viện cần cài đặt

```

## Hướng dẫn chạy project
1. Huấn luyện mô hình

Chạy pipeline xử lý dữ liệu, huấn luyện và calibration:
```
python src/main.py
```
Sau khi chạy thành công, hệ thống sẽ:
```
Làm sạch dữ liệu
Tiền xử lý dữ liệu
Huấn luyện Logistic Regression
Thực hiện Platt Scaling
Thực hiện Isotonic Regression
Sinh biểu đồ đánh giá
Lưu model tại src/models/
```
Các file được sinh:
```
model_baseline.pkl
model_platt.pkl
model_iso.pkl
scaler.pkl
encoders.pkl
features.pkl
```
2. Chạy demo dự đoán
```bash
python demo.py
```
Hệ thống hỗ trợ:
Dự đoán từ file data_sample.csv
Test flow BENIGN ngẫu nhiên (Từ tập Test)
Test flow ATTACK ngẫu nhiên (từ tập Test)

## Quy ước làm việc

1. KHÔNG thay đổi cấu trúc thư mục gốc
2. KHÔNG push code lỗi, code không chạy được
3. Commit rõ chức năng thực hiện
4. Pull origin main trước khi push code mới

## Tổng quan nhánh
### main
Nhánh chính, chứa code mới, ổn định, không commit trực tiếp trên nhánh này
### Các nhánh làm việc
1. Tạo từ main
2. Quy ước đặt tên: 
``` 
Chức năng mới: feature/ten-chuc-nang
Sửa lỗi: fix/ten-chuc-nang
```
### Bắt đầu chức năng mới 
```
git checkout main
git pull origin main
git checkout -b feature/ten-chuc-nang
```
### Push code & Pull Request
```
git push origin feature/ten-chuc-nang 
```
*Nhánh đã PR lần sau chỉ cần git push



