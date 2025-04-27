from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required
from . import auth_blueprint
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, OTPForm, ResetPasswordForm
from app.models.user import User
from app.models.role import Role
from app.flask_extensions import csdl


#Tạo route /auth/login cho login
@auth_blueprint.route('/login', methods=['GET', 'POST']) #mở form, submit form

#hàm login
def login():
    form = LoginForm() #auth/forms.py

    #nếu form đc gửi post và hợp lệ =>tìm user csdl trùng user input
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #nếu user tồn tại, pass đúng 
        if user and user.check_password(form.password.data): #models/user: check_password
            login_user(user, remember=form.remember.data) #remember = true/false - luu login or k
            return redirect(url_for('home.homepage'))  # thumuc.ten def
        flash('Username hoặc Password không hợp lệ!', 'danger') #mess
    
    # k là post || form k h.le => reload
    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/admin-login', methods=['GET', 'POST']) 
def adminLogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() 
        if user and user.check_password(form.password.data): # + role là 1 admin
            login_user(user, remember=form.remember.data) #remember = true/false - luu login or k
            return redirect(url_for('admin.adminPage'))
        flash('Username hoặc Password không hợp lệ!', 'danger') 
    return render_template('auth/adminLogin.html', form=form)
    
#route xly đăng ký auth/register
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #form đc post, h.le
        #neu username input trung username csdl => reload register page
        if User.query.filter_by(username=form.username.data).first():
            flash('Đã tồn tại Username!', 'warning')
            return redirect(url_for('auth.register'))

        # k trung thi tao user moi 
        new_user = User(username=form.username.data, fullname = form.fullname.data, email=form.email.data, sdt = form.sdt.data)
        new_user.set_password(form.password.data)
        csdl.session.add(new_user) #luu vao csdl

        csdl.session.flush()  # Lấy user.id trước khi commit


        # Gán vai trò "member" (role_id = 2) vào bảng user_role
        member_role = Role.query.get(2)  # Lấy vai trò có id = 2
        if member_role:
            new_user.roles.append(member_role)  # Thêm vai trò vào mối quan hệ

        csdl.session.commit()
        flash('Đăng ký thành công! Quay về đăng nhập', 'success') #kieu flash success
        logout_user()  # clear session
        return redirect(url_for('auth.login')) #chuyen hg ve login page 
    
    return render_template('auth/register.html', form=form) # k là post || form k h.le => reload


@auth_blueprint.route('/logout')
@login_required #b buoc login
def logout(): 
    logout_user() #xoa session 
    flash('Bạn đã Đăng xuất!', 'info')
    return redirect(url_for('auth.login'))

# _____Forgot pass_____
import random
def generate_otp():
    return str(random.randint(100000, 999999))

from flask_mail import Message
from flask import current_app
def send_otp_email(to_email, otp):
    
    if current_app.config['MAIL_USERNAME'] == 'your_email@gmail.com':
        print(f"OTP của {to_email} là: {otp}")
    else:
        mail = current_app.extensions.get('mail')
        msg = Message('Mã OTP của bạn', sender='your_email@gmail.com', recipients=[to_email])
        msg.body = f'Mã OTP của bạn là {otp}. Thời gian hiệu lực là 10 phút.'
        mail.send(msg) 

from datetime import datetime, timedelta, timezone
now = datetime.now(timezone.utc)
otp_timeout = (now + timedelta(minutes=10))

@auth_blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data).first() #tim user , email khop vs input form
        if user:
            otp = generate_otp()
            # Lưu OTP và thời gian hết hạn vào session thay vì cơ sở dữ liệu
            session['reset_otp'] = otp
            session['reset_user_id'] = user.id  # Lưu user_id để xác minh sau này
            
            csdl.session.commit()
            send_otp_email(user.email, otp)
            flash('1 mã OTP đã được gửi đến email của bạn. Hãy nhập OTP!', 'success')
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Username hoặc Password không tồn tại!', 'danger')
    else:
        print("not form validate_on_submit")

    return render_template('auth/forgotPassword.html', form=form)
    

@auth_blueprint.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()
    if form.validate_on_submit():
        user_id = session.get('reset_user_id')
        otp = session.get('reset_otp')
        user = User.query.get(user_id)
        if user and otp == form.otp.data and now < otp_timeout:
            session['otp_verified'] = True
            flash('Xác thực OTP thành công! Đặt lại mật khẩu', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash('OTP không hợp lệ!', 'danger')
    return render_template('auth/verify_otp.html', form=form)

@auth_blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    # chua xac minh otp thi ve lai forgot pass page 
    if not session.get('otp_verified'):
        return redirect(url_for('auth.forgot_password'))
    form = ResetPasswordForm()

    #form hop le
    if form.validate_on_submit():
        user_id = session.get('reset_user_id')

        #truy van tu csdl theo user id
        current_user = User.query.get(user_id)
        current_user.set_password(form.password.data)
        
        csdl.session.commit() #luu csdl

        #delete khoi session
        session.pop('reset_user_id', None)
        session.pop('otp_verified', None)
        session.pop('reset_otp', None)
        session.pop('otp_timeout', None)
        flash('Đã đặt lại mật khẩu! Hãy đăng nhập!', 'success')
        return redirect(url_for('auth.login'))  # Điều hướng đến trang login
    return render_template('auth/resetPassword.html', form=form)