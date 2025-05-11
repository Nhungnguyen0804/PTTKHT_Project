from app.flask_extensions import csdl, login_manager

class Category(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    category_name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...