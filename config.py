# Cấu hình ứng dụng

# config.py
import os

from flask import current_app
class Config:
    
    mail_string = 'your_email@gmail.com'
    mail_pass_string = 'your_app_password'  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Cấu hình Mail cố định
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = mail_string# <-- Thay bằng email thật
    MAIL_PASSWORD =  mail_pass_string  # <-- Thay bằng App password thật

    #cau hinh upload
    MAX_CONTENT_LENGTH =  20 * 1024 * 1024  # Giới hạn 2MB ảnh
