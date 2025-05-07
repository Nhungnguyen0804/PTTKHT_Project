import os
from flask import render_template, flash, redirect, url_for,request , current_app
from flask_login import  login_required, current_user, logout_user
from . import accManagement_blueprint
from app.models.user import User, user_role
from app.models.role import Role
from app.flask_extensions import csdl
from .forms import changePasswordForm, editProfileForm
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_TYPES = {'png', 'jpg', 'jpeg', 'gif'}
def get_user_type(username):
    if username.startswith('hs'):
        return 'Học sinh'
    elif username.startswith('gv'):
        return 'Giáo viên'
    elif username.startwith('admin'):
        return 'Admin'
    else:
        return 'Khác'
    
#Tạo route 
@accManagement_blueprint.route('/account/profile')
@login_required
def view_profile():
    
    # Cập nhật user mới nhất từ DB
    user = csdl.session.get(User, current_user.id)
    user_type = get_user_type(user.get_username())
    
    return render_template('accountManagement/profile.html', user=user, user_type = user_type)

@accManagement_blueprint.route('/account/change-password',methods=['GET', 'POST'])
@login_required
def change_password():
    # Cập nhật user mới nhất từ DB
    user = csdl.session.get(User, current_user.id)
    
    form= changePasswordForm()
    if form.validate_on_submit(): # form hop le
        if user.check_password(form.current_password.data): # dung mat khau hien tai => cho phep doi pass
            if form.new_password.data == form.confirm_password.data:
                user.set_password(form.new_password.data)
                csdl.session.commit()
                flash('Đã đặt lại mật khẩu!', 'success')
            
        else:
            flash('Mật khẩu hiện tại không đúng!', 'danger')
        
    return render_template('accountManagement/changePassword.html', form=form, user=user)
    
    


    
@accManagement_blueprint.route('/account/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    user_type = get_user_type(user.get_username())
    form = editProfileForm()

    if form.validate_on_submit():
        user.set_fullname(form.hoTen.data)
        # user.set_avatar()
        user.set_date_of_birth(form.ngaySinh.data)
        user.set_gender(form.gioiTinh.data)
        user.set_address(form.address.data)
        user.set_email(form.email.data)
        user.set_phone(form.phone.data)
        user.set_facebook(form.fb.data)
        user.set_zalo(form.zalo.data)
        
        csdl.session.commit()
        flash('Hồ sơ đã được cập nhật!', 'success')
        return redirect(url_for('accountManagement.edit_profile'))
    # GÁN DỮ LIỆU TỪ DB VÀO FORM (chỉ khi GET)
    elif request.method == 'GET':
        form.hoTen.data = user.get_fullname()
        form.ngaySinh.data = user.get_date_of_birth()
        form.gioiTinh.data = user.get_gender()
        form.address.data = user.get_address()
        form.email.data = user.get_email()
        form.phone.data = user.get_phone()
        form.fb.data= user.get_facebook()
        form.zalo.data = user.get_zalo()

    return render_template('accountManagement/editProfile.html', form=form, user=user , user_type = user_type)


@accManagement_blueprint.route('/account/delete-account')
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    if user:
        logout_user()  # đăng xuất trước khi xóa
        csdl.session.delete(user)
        csdl.session.commit()
        flash("Bạn đã xóa tài khoản!", "info")
    return redirect(url_for('auth.login'))  



#upload
# Kiểm tra đuôi file
def allowed_file(filename):
    # tên file chứa dấu . và phần tử sau dấu chấm thuộc ALLOWED_IMAGE_TYPES
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_TYPES


@accManagement_blueprint.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar_input_name' not in request.files:
        flash('Không có file ảnh.')
        return redirect(url_for('accountManagement.edit_profile'))

    file = request.files['avatar_input_name']

    if file.filename == '':
        flash('Bạn chưa chọn ảnh!')
        return redirect(url_for('accountManagement.edit_profile'))

    if file and allowed_file(file.filename):
        # Lấy đuôi file
        duoi_file = file.filename.rsplit('.', 1)[1].lower()

        # Đổi tên file theo username, vd: user_hs0001.jpg
        filename = f"user_{secure_filename(current_user.username)}.{duoi_file}"
        print(filename)
        UPLOAD_FOLDER =os.path.join(current_app.root_path, 'static', 'image', 'avatar_upload')
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Ghi đè nếu đã tồn tại
        file.save(filepath)

        # Tạo link ảnh (vd: /static/image/avatar_upload/user_hs00001.jpg)
        avatar_url = url_for('static', filename=f'image/avatar_upload/{filename}')

        # Cập nhật vào CSDL
        user = User.query.get(current_user.id)
        user.set_avatar(avatar_url)
        csdl.session.commit()

        flash('Đã cập nhật ảnh đại diện!', 'success')
    else:
        flash('File không hợp lệ (chỉ nhận png, jpg, jpeg, gif)!' ,'danger')

    return redirect(url_for('accountManagement.edit_profile'))
