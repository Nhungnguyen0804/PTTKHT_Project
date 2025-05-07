import os
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import post_blueprint 
from app.models.post import Post
from app import csdl
import uuid



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route tạo bài đăng mới
@post_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content')
        post_type = request.form.get('post_type')
        price = request.form.get('price')
        contact = request.form.get('contact')
        images = request.files.getlist('images')

        if not content:
            flash('Nội dung bài viết không được để trống.', 'danger')
            return redirect(url_for('post.create_post'))

        if not post_type:
            flash('Vui lòng chọn loại bài đăng.', 'danger')
            return redirect(url_for('post.create_post'))

        if post_type == 'thanh_ly' and (not price or not contact):
            flash('Thanh lý yêu cầu điền giá và thông tin liên hệ.', 'danger')
            return redirect(url_for('post.create_post'))

        if post_type in ('trao_doi', 'donate') and not contact:
            flash('Vui lòng nhập thông tin liên hệ.', 'danger')
            return redirect(url_for('post.create_post'))

        image_urls = []
        # Thư mục lưu ảnh upload
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads')
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

        # Ghép thêm thông tin loại bài, giá và liên hệ vào content
        extra_info = ""
        if post_type == 'thanh_ly':
            extra_info += f"\nGiá: {price}"
        if contact:
            extra_info += f"\nLiên hệ: {contact}"

        type_mapping = {
        'thanh_ly': 'Thanh Lý',
        'trao_doi': 'Trao Đổi',
        'donate': 'Donate'
        }

        full_content = f"[{type_mapping.get(post_type, post_type)}]\n{content}{extra_info}"
        
        new_post = Post(
            post_id=str(uuid.uuid4()),
            content=full_content,
            image_url=image_url_str,
            is_approved=is_approved,
            status = 'Not done',  # Trạng thái mặc định
            user_id=current_user.id,  # Lưu ID của người dùng hiện tại
            post_type = type_mapping.get(post_type, post_type)  # Lưu loại bài đăng

        )

        csdl.session.add(new_post)
        csdl.session.commit()

        flash(
            'Bài viết đã được đăng thành công!' if current_user.roles == 'admin'
            else 'Bài viết đã được gửi và đang chờ duyệt. Vui lòng đợi admin xét duyệt.',
            'success'
        )
        
        # Thay đổi từ render_template sang redirect
        return redirect(url_for('post.my_posts'))

    return render_template('post/create_post.html')

# Route đánh dấu bài viết là đã hoàn tất
@post_blueprint.route('/mark_done', methods=['POST'])
@login_required
def mark_done():
    post_id = request.form.get('post_id')

    if not post_id:
        flash('Không tìm thấy bài viết.', 'danger')
        return redirect(url_for('post.view_posts'))

    post = Post.query.filter_by(post_id=post_id).first()

    if not post:
        flash('Bài viết không tồn tại.', 'danger')
        return redirect(url_for('post.view_posts'))

    # Chỉ cho phép đánh dấu nếu là admin hoặc chủ bài viết (nếu có user_id trong bảng Post)
    if current_user.roles != 'admin' and post.user_id != current_user.id:
        flash('Bạn không có quyền thay đổi trạng thái bài viết này.', 'danger')
        return redirect(url_for('post.view_posts'))

    post.status = 'Done'
    csdl.session.commit()
    flash('Bài viết đã được đánh dấu là hoàn tất.', 'success')
    return redirect(url_for('post.my_posts'))


# Route xem các bài đăng của user hiện tại
@post_blueprint.route('/my_posts')
@login_required
def my_posts():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.is_approved.desc()).all()
    return render_template('post/my_posts.html', posts=posts)

# Route xóa bài viết
@post_blueprint.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    post_id = request.form.get('post_id')
    post = Post.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if not post:
        flash('Không tìm thấy bài viết hoặc bạn không có quyền xóa.', 'danger')
        return redirect(url_for('post.my_posts'))

    csdl.session.delete(post)
    csdl.session.commit()
    flash('Bài viết đã được xóa.', 'success')
    return redirect(url_for('post.my_posts'))

# Route sửa bài viết
@post_blueprint.route('/edit/<string:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id and not current_user.has_role('admin'):
        flash("Bạn không có quyền sửa bài này.", "danger")
        return redirect(url_for('post.my_posts'))

    if request.method == 'POST':
        post.content = request.form['content']
        # Cập nhật thêm image_url nếu có
        csdl.session.commit()
        flash("Bài đăng đã được cập nhật.", "success")
        return redirect(url_for('post.my_posts'))

    return render_template('post/edit_post.html', post=post)

