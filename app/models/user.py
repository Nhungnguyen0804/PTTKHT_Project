from flask_login import UserMixin
from app.flask_extensions import csdl, login_manager
# Bảng liên kết User_Role (many-to-many)
user_role = csdl.Table('user_role',
    csdl.Column('user_id', csdl.Integer, csdl.ForeignKey('user.id'), primary_key=True),
    csdl.Column('role_id', csdl.Integer, csdl.ForeignKey('role.id'), primary_key=True)
)
class Role(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...

class User(UserMixin, csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    username = csdl.Column(csdl.String(50), unique=True, nullable=False)
    email = csdl.Column(csdl.String(120), unique=True, nullable=False)
    password  = csdl.Column(csdl.String(128), nullable=False)
    roles = csdl.relationship('Role', secondary=user_role, backref=csdl.backref('users', lazy='dynamic'))

    #set pass = hàm tạo mã hóa pass của pass ban đầu
    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    #user có vai trò gì (admin, member)
    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
