# config.py
import os


class Config:
    
    mail_string = 'your_email@gmail.com'
    mail_pass_string = 'your_app_password'  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey123'
    
    # Sử dụng PostgreSQL thay cho SQLite
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/reusebox'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cấu hình Mail cố định
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = mail_string
    MAIL_PASSWORD = mail_pass_string
