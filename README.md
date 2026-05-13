## Đề tài: 29 - Hiệu chỉnh xác suất dự đoán cho IDS nhị phân trên bộ dữ liệu CICIDS2017

## Hướng dẫn cài đặt

1. Clone dự án: `git clone [LINK_DỰ_ÁN]`
2. Cài đặt các Extension cần thiết: Black Formatter, Jupyter, Pylance
3. Kích hoạt môi trường ảo: `.\venv\Scripts\activate`
4. Cài thư viện: `pip install -r requirements.txt`

## Quy ước làm việc

1. KHÔNG thay đổi cấu trúc thư mục
2. KHÔNG push code lỗi, code không chạy được
3. Commit rõ phần bản thân làm

## Tổng quan nhánh
### main
Nhánh chính, chứa code mới, ổn định, không commit trực tiếp trên nhánh này
### Các nhánh làm việc
1. Tạo từ main
2. Quy ước đặt tên: feature/ten-chuc-nang
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



## Cấu trúc thư mục

```
project/
├── data/
│ ├── raw/                  #Lưu dữ liệu gốc
│ └── processed/            #Lưu dữ liệu đã xử lý
├── notebooks/              #Lưu notebook thử nghiệm
├── src/                    #Lưu code xử lý chính
├── results/                #Lưu bảng kết quả và biểu đồ
├── report/
└── requirements.txt        # Ghi các thư viện cần cài đặt

```
