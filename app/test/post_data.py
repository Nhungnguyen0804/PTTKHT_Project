import os
import sqlite3
import random
import string
from datetime import datetime, timedelta


# Xác định thư mục hiện hành (chứa script này)
current_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
db_path = os.path.join(project_dir, 'instance', 'app_database.db')
print("Database path:", db_path)

# ================== HÀM TẠO DỮ LIỆU NGẪU NHIÊN ==================

def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def random_bool():
    return random.choice([0, 1])


def random_type():
    return random.choice(["Thanh Lý", "Trao Đổi", "Donate"])


def random_status():
    return random.choice(["Done", "Not Done"])

def random_date(start_year=2020):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d %H:%M:%S')


# def random_create_date():
#     days_ago = random.randint(0, 30)
#     random_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
#     return random_time.strftime('%Y-%m-%d %H:%M:%S')

def random_category_id():
    return random.randint(1, 20)  # Giả sử có 20 category

def random_interest_users():
    ids = [str(random.randint(1, 20)) for _ in range(random.randint(0, 3))]
    return ",".join(set(ids))

# ================== HÀM TẠO POST ==================

def generate_post():
    post_id = random_string()
    content = "Bài đăng mẫu " + random_string(8)
    image_url = "/static/uploads/" + random_string(10) + ".jpg"
    is_approved = random_bool()
    status = random_status()
    post_type = random_type()
    create_date = random_date()
    user_id = random.randint(1, 400)
    category_id = random_category_id()
    interest_count = random.randint(0, 500)
    interested_user_id = random_interest_users()

    return (post_id, content, image_url, is_approved, status, post_type, create_date, user_id, category_id, interest_count, interested_user_id)

# ================== THÊM DỮ LIỆU VÀO DATABASE ==================

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

n = int(input("Nhập số lượng post muốn thêm: "))

for _ in range(n):
    post = generate_post()
    cursor.execute('''
        INSERT INTO post (
            post_id, content, image_url, is_approved, status, post_type, create_date,
            user_id, category_id, interest_count, interested_user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', post)

conn.commit()
conn.close()
print(f"✅ Đã thêm {n} post vào cơ sở dữ liệu.")

