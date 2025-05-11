from flask_login import UserMixin
from app.flask_extensions import csdl, login_manager
from datetime import datetime


class User(UserMixin, csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    username = csdl.Column(csdl.String(50), unique=True, nullable=False)
    password  = csdl.Column(csdl.String(128), nullable=False)
    avatar = csdl.Column(csdl.Text, nullable = True)
    fullname = csdl.Column(csdl.String(120), nullable=False)
    date_of_birth = csdl.Column(csdl.Date, nullable = True)
    gender = csdl.Column(csdl.String(10), nullable = True)
    address = csdl.Column(csdl.Text, nullable = True)
    
    email = csdl.Column(csdl.String(120), unique=True, nullable=False)
    phone = csdl.Column(csdl.String(20), nullable=True) #co the null
    facebook = csdl.Column(csdl.Text, nullable =True)
    roles = csdl.relationship('Role', secondary='user_role', backref=csdl.backref('users', lazy='dynamic'))
    created_date = csdl.Column(csdl.DateTime, default=datetime.utcnow)  # Thêm dòng này
    def set_avatar(self, avatar):
        self.avatar = avatar
    def get_avarar(self):
        return self.avatar
    
    def set_username(self, username):
        self.username=username
    def get_username(self):
        return self.username

    def set_fullname(self, fullname):
        self.fullname = fullname
    def get_fullname(self):
        return self.fullname
    
    def set_gender(self,gender):
        self.gender=gender
    def get_gender(self):
        return self.gender
    
    def set_date_of_birth(self,date_of_birth):
        self.date_of_birth = date_of_birth
    def get_date_of_birth(self):
        return self.date_of_birth
    
    def set_address(self, address):
        self.address = address
    def get_address(self):
        return self.address
    
    def set_email(self,email):
        self.email=email
    def get_email(self):
        return self.email
    
    def set_phone(self,phone):
        self.phone=phone
    def get_phone(self):
        return self.phone
    
    def set_facebook(self, facebook):
        self.facebook=facebook
    def get_facebook(self):
        return self.facebook
    
    def set_zalo(self, zalo):
        self.zalo=zalo
    def get_zalo(self):
        return self.zalo
    
    #set pass = hàm tạo mã hóa pass của pass ban đầu
    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password
    def check_password(self, password):
        return self.password == password
    
    #user có vai trò gì (admin, member)
    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
    
    def get_role(self):
        return ', '.join(role.name for role in self.roles)

# Bảng liên kết User_Role (many-to-many)
user_role = csdl.Table('user_role',
    csdl.Column('user_id', csdl.Integer, csdl.ForeignKey('user.id'), primary_key=True),
    csdl.Column('role_id', csdl.Integer, csdl.ForeignKey('role.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id): #luu ttin user by id da luu trong session login 
    return User.query.get(int(user_id)) #doi tuong User chua ttin (username, pass,email, ...)
