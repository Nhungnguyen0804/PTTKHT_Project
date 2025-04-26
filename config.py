# Cấu hình ứng dụng

# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
