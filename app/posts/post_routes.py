from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import post_blueprint 
from app.models.post import Post
from app import csdl
import uuid
import os

# Thư mục lưu ảnh upload
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route tạo bài đăng mới
@post_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content')
        images = request.files.getlist('images')  # Lấy tất cả file ảnh từ input có multiple

        if not content:
            flash('Nội dung bài viết không được để trống.', 'danger')
            return redirect(url_for('post.create_post')) 

        image_urls = []  # Danh sách URL các ảnh hợp lệ
        for image_file in images:
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                image_file.save(save_path)
                image_urls.append(f'/static/uploads/{unique_filename}')

        image_url_str = ','.join(image_urls) if image_urls else None

        is_approved = True if current_user.roles == 'admin' else False

        new_post = Post(
            post_id=str(uuid.uuid4()),
            content=content,
            image_url=image_url_str,
            is_approved=is_approved
        )

        csdl.session.add(new_post)
        csdl.session.commit()

        # Sau khi tạo bài viết và commit
        success_message = (
            'Bài viết đã được đăng thành công!' if current_user.roles == 'admin'
            else 'Bài viết đã được gửi và đang chờ duyệt. Vui lòng đợi admin xét duyệt.'
        )

        return render_template('post/create_post.html',
            success_message=success_message,
            user_role=current_user.roles
        )

    # Trường hợp GET hoặc không phải POST
    return render_template('post/create_post.html')

# Route xem tất cả bài viết đã được duyệt
@post_blueprint.route('/posts')
def view_posts():
    posts = Post.query.filter_by(is_approved=True).all()
    return render_template('post/view_posts.html', posts=posts)
