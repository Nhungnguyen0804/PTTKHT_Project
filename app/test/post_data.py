import os
import sqlite3
import random
import string
from datetime import datetime, timedelta
# Xác định thư mục hiện hành (chứa user_data.py)
current_dir = os.path.abspath(os.path.dirname(__file__))

# Xác định thư mục gốc dự án bằng cách lên hai cấp từ current_dir
project_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

# Tạo đường dẫn đến file SQLite trong thư mục instance
db_path = os.path.join(project_dir, 'instance', 'app_database.db')
print(db_path)

# Hàm tạo chuỗi ngẫu nhiên
def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
def random_0_1():
    return random.randint(0, 1)

def random_type():
    return random.choice(["Thanh Lý", "Trao Đổi", "Donate"])



# Hàm tạo user ngẫu nhiên
def generate_post(index):
    post_id = random_string()
    content = random_string()
    image_url = "/static/image/avatar.png"
    is_approved = random_0_1()
    user_id = random.randint(1,400)
    post_type = random_type()

    return (post_id,content, image_url, is_approved, user_id,post_type)



# Kết nối cơ sở dữ liệu
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Nhập số lượng user muốn thêm
n = int(input("Nhập số lượng post muốn thêm: "))

# Thêm n user
for i in range(n):
    post = generate_post(i + 1)
    # user = generate_gv(i+1)
    cursor.execute('''
    INSERT INTO post (post_id,content, image_url, is_approved, user_id,post_type)
    VALUES (?, ?, ?, ?,?,?)
    ''', post)
    

conn.commit()
conn.close()
print(f"Đã thêm {n} post vào cơ sở dữ liệu.")
