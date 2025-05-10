from asyncio.windows_events import NULL
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
import pytz

from app import userManagement
from app.models.post import Post
from app.models.role import Role
from app.models.category import Category
from app.flask_extensions import csdl as db

postManagement_blueprint = Blueprint('postManagement', __name__, template_folder='templates')

@postManagement_blueprint.route('/admin/posts')
def manage_post():
    if current_user.has_role('admin'):
        posts = Post.query.all()
        return render_template('postManagement/post_manage.html', posts=posts)
    else:
        flash('Username không phải là admin!', 'danger')
        return redirect(url_for('auth.adminLogin'))

@postManagement_blueprint.route('/admin/posts/delete/<post_id>', methods=['POST', 'GET'])
def delete_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        flash('Bài viết không tồn tại!', 'danger')
        return redirect(url_for('postManagement.manage_post'))

    db.session.delete(post)
    db.session.commit()
    flash('Đã xóa bài viết thành công!', 'success')
    return redirect(url_for('postManagement.manage_post'))

@postManagement_blueprint.route('/admin/posts/edit/<post_id>', methods=['POST'])
def approve_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        flash('Bài viết không tồn tại!', 'danger')
        return redirect(url_for('postManagement.manage_post'))

    if not post.is_approved and not post.approval_date:
        post.is_approved = True
        post.approval_date = datetime.now(pytz.utc)
        db.session.commit()
        flash('Đã duyệt bài viết thành công!', 'success')
    else:
        flash('Bài viết đã được duyệt trước đó!', 'warning')

    return redirect(url_for('postManagement.manage_post'))