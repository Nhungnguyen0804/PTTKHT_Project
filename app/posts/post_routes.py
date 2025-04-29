from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import post_blueprint 
from app.models.post import Post
import uuid

# Route tạo bài đăng mới
@post_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        content = request.form.get('content')
        image_url = request.form.get('image_url')

        # Kiểm tra dữ liệu
        if not content:
            flash('Nội dung bài viết không được để trống.', 'danger')
            return redirect(url_for('post.create_post'))

        # Xác định trạng thái duyệt dựa trên vai trò người dùng
        is_approved = True if current_user.role == 'admin' else False

        # Tạo bài viết mới
        new_post = Post(
            post_id=str(uuid.uuid4()),   # Tạo ID ngẫu nhiên
            content=content,
            image_url=image_url,
            is_approved=is_approved
        )

        Post.session.add(new_post)
        Post.session.commit()

        if is_approved:
            flash('Bài viết đã được đăng thành công!', 'success')
        else:
            flash('Bài viết đã gửi thành công, vui lòng đợi admin duyệt.', 'info')

        return redirect(url_for('posts.view_posts.html'))

    return render_template('post/create_post.html')


# Route xem tất cả bài viết đã được duyệt
@post_blueprint.route('/posts')
def view_posts():
    # Chỉ hiển thị bài viết đã được admin duyệt
    posts = Post.query.filter_by(is_approved=True).all()
    return render_template('posts/view_post.html', posts=posts)


