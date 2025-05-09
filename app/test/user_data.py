import os
import sqlite3
import random
import string

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

# Hàm tạo user ngẫu nhiên
def generate_user(index):
    username = f"hs00{index}"
    password = "123456"
    avatar = "/static/image/avatar.png"
    fullname = f"User {index}"
    date_of_birth = "2000-01-01"
    gender = "male"
    address = None
    email = f"user{index}@example.com"
    phone = f"0123{str(index).zfill(5)}"
    facebook = None
    zalo = None
    return (username, password, avatar, fullname, date_of_birth, gender, address, email, phone, facebook, zalo)

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Nhập số lượng user muốn thêm
n = int(input("Nhập số lượng user muốn thêm: "))

# Thêm n user
for i in range(n):
    user = generate_user(i + 1)
    cursor.execute('''
        INSERT INTO user (username, password, avatar, fullname, date_of_birth, gender, address, email, phone, facebook, zalo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', user)
    user_id = cursor.lastrowid  # Lấy id vừa insert tự động

    # Gán role_id = 2 trong bảng user_role
    cursor.execute('''
        INSERT INTO user_role (user_id, role_id)
        VALUES (?, 2)
    ''', (user_id,))

conn.commit()
conn.close()
print(f"Đã thêm {n} user vào cơ sở dữ liệu.")
