import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_eda_plots(df, save_dir="./results"):
    print("ĐANG VẼ BIỂU ĐỒ VÀ LƯU VÀO THƯ MỤC results/...")
    
    # Kiểm tra và tạo thư mục results/ nếu chưa có
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Biểu đồ 1: Phân bố nhãn (Label Distribution)
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="Label", palette="Set2")
    plt.title("Phân bố nhãn (0: Normal, 1: Attack)")
    plt.xlabel("Nhãn (0 = Bình thường, 1 = Tấn công)")
    plt.ylabel("Số lượng mẫu")
    
    path_1 = os.path.join(save_dir, "label_distribution.png")
    plt.savefig(path_1, bbox_inches="tight", dpi=300)
    print(f"- Đã lưu biểu đồ 1 tại: {path_1}")
    plt.close()
    
    # Biểu đồ 2: Phân bố Flow Duration theo nhãn
    # Boxplot giúp thấy rõ sự khác biệt về thời gian duy trì luồng mạng giữa 2 nhãn
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="Label", y="Flow Duration", palette="Set2")
    plt.yscale("log") # Dùng thang đo log vì số liệu mạng chênh lệch rất lớn
    plt.title("Phân bố Flow Duration theo Nhãn (Thang đo Log)")
    plt.xlabel("Nhãn (0 = Bình thường, 1 = Tấn công)")
    plt.ylabel("Flow Duration (Log Scale)")
    
    path_2 = os.path.join(save_dir, "flow_duration_boxplot.png")
    plt.savefig(path_2, bbox_inches="tight", dpi=300)
    print(f"- Đã lưu biểu đồ 2 tại: {path_2}")
    plt.close()

    print("Hoàn tất vẽ biểu đồ!\n")