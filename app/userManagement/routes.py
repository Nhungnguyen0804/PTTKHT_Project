from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app import userManagement
from app.models.user import User
from app.models.role import Role
from app.flask_extensions import csdl as db

userManagement_blueprint = Blueprint('userManagement', __name__, template_folder='templates')


@userManagement_blueprint.route('/admin/users')
def manage_user():
    if current_user.has_role('admin'):
        users = User.query.all()
        return render_template('userManagement/manage_user.html', users=users)
    else:
        flash('Username không phải là admin!', 'danger')
        return redirect(url_for('auth.adminLogin'))


@userManagement_blueprint.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == current_user.username:
        flash('Cannot edit your own account!', 'danger')
        return redirect(url_for('userManagement.manage_user'))
    if user.username == 'root':
        flash('Cannot edit root account!', 'danger')    
        return redirect(url_for('userManagement.manage_user'))
    if user.has_role('admin') and current_user.username != 'root':
        flash('Cannot edit admin account!', 'danger')       
        return redirect(url_for('userManagement.manage_user'))    
    if request.method == 'POST':
        user.username = request.form['username']
        if request.form['password']:
            user.password = request.form['password']
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('userManagement.manage_user'))
    return render_template('userManagement/manage_user.html', action="Edit", user=user)

@userManagement_blueprint.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname'] 
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        if User.query.filter_by(username=username).first():
            flash('Username đã tồn tại!', 'danger')
            all_roles = Role.query.all()
            return render_template('userManagement/manage_user.html', action="Create", roles=all_roles)
        new_user = User(username=username, password=password, fullname=fullname, email=email, phone=phone, address=address)
        # Thêm các trường khác nếu cần
        default_role = Role.query.filter_by(name='member').first()
        new_user.roles = [default_role]
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('userManagement.manage_user'))
    all_roles = Role.query.all()
    return render_template('userManagement/manage_user.html', action="Create", roles=all_roles)

@userManagement_blueprint.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == current_user.username:
        flash('Cannot delete your own account!', 'danger')
        return redirect(url_for('userManagement.manage_user'))
    if user.username == 'root':
        flash('Cannot delete root account!', 'danger')
        return redirect(url_for('userManagement.manage_user'))
    # Nếu là root thì có thể xóa bất kỳ ai kể cả admin
    if current_user.username == 'root':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!')
        return redirect(url_for('userManagement.manage_user'))

    # Nếu không phải root, không được xóa user có vai trò admin
    if user.has_role('admin'):
        flash('Cannot delete admin account!', 'danger')
        return redirect(url_for('userManagement.manage_user'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('userManagement.manage_user'))


@userManagement_blueprint.route('/search-user', methods=['GET', 'POST'])
def search_user():
    user = None
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:
            user = User.query.filter_by(username=user_name).first()
            if not user:
                flash('Không tìm thấy người dùng với tên này!', 'warning')
        else:
            flash('Vui lòng nhập tên người dùng để tìm kiếm!', 'warning')
    users = User.query.all()
    return render_template('userManagement/manage_user.html', user=user, users=users, action='Search')