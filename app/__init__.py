# Khởi tạo Flask app và register các Blueprint

from flask import Flask
from flask_login import current_user
from flask_mail import Mail
from .flask_extensions import csdl, login_manager, migrate
from .auth import auth_blueprint
from .home import home_blueprint
from .test import test_blueprint
from .admin import admin_blueprint
from .accountManagement import accManagement_blueprint
from .posts import post_blueprint
from .userManagement import userManagement_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') #tải cấu hình từ lớp config từ file config.py

    mail = Mail(app)
    # Khởi tạo SQLAlchemy trước, đảm bảo csdl sẵn sàng migrate
    csdl.init_app(app)
    
    # Khởi tạo các extension khác
    login_manager.init_app(app)#init quản lý login
    migrate.init_app(app, csdl)#init quản lý thay đổi schema csdl
   

    # Import các model để đăng ký với SQLAlchemy
    from .models.user import User, user_role  # Import cả User và user_role
    from .models.role import Role, init_roles
    

    # Tạo các bảng trong csdl (chỉ cần cho lần đầu)
    with app.app_context():
        csdl.create_all()
        init_roles()# Khởi tạo gt bang role
    
    # Đăng ký các blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(test_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(accManagement_blueprint)
    app.register_blueprint(userManagement_blueprint)

    # Thiết lập route cho trang đăng nhập
    login_manager.login_view = 'auth.login'

    app.jinja_env.globals.update(has_role=User.has_role)

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app

