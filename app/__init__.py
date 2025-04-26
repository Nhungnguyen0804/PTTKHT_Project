# Khởi tạo Flask app và register các Blueprint

from flask import Flask
from .flask_extensions import csdl, login_manager, migrate
from .auth import auth_blueprint
from .home import home_blueprint
from .test import test_blueprint
from .admin import admin_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') #tải cấu hình từ lớp config từ file config.py

    csdl.init_app(app) #connect flask - SQLAlchemy
    with app.app_context():
        csdl.create_all()
        
    login_manager.init_app(app) #init quản lý login
    migrate.init_app(app, csdl) #init quản lý thay đổi schema csdl 

    
    from .models import user  # Đảm bảo import model trước khi migrate

    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(test_blueprint)
    app.register_blueprint(auth_blueprint)

    login_manager.login_view = 'auth.login'
    return app

