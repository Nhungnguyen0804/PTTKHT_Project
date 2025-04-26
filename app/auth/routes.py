from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth_blueprint
from .forms import LoginForm, RegisterForm
from app.models.user import User
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
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        csdl.session.add(new_user) #luu vao csdl
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
