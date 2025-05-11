import os
from flask import render_template, request, redirect, url_for, flash, current_app,jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import post_blueprint 
from app.models.post import Post
from app.models.user import User
from app import csdl
import uuid
import os
from datetime import datetime
import pytz
from app.models.category import Category
from .form import FilterForm

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route tạo bài đăng mới
@post_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    categories = Category.query.all()
    if request.method == 'POST':
        content = request.form.get('content')
        post_type = request.form.get('post_type')
        price = request.form.get('price')
        # contact = request.form.get('contact')
        phone = request.form.get('phone')
        email = request.form.get('email')
        facebook = request.form.get('facebook')
        images = request.files.getlist('images')
        category_id = request.form.get('category')

        if not content:
            flash('Nội dung bài viết không được để trống.', 'danger')
            return redirect(url_for('post.create_post'))

        if not post_type:

            return redirect(url_for('post.create_post'))

        if post_type in ('trao_doi', 'donate') and not phone and not email and not facebook:
            flash('Vui lòng nhập thông tin liên hệ.', 'danger')
            return redirect(url_for('post.create_post'))

        # Tạo bài post trước để có post_id
        type_mapping = {
            'thanh_ly': 'Thanh Lý',
            'trao_doi': 'Trao Đổi',
            'donate': 'Donate'
        }

        extra_info = ""
        if post_type == 'thanh_ly':
            extra_info += f"\nGiá: {price}"

        extra_info += f"\nLiên hệ:"
        if phone:
            extra_info += f"\nSố điện thoại:{phone}"
        if email:
            extra_info += f"\nEmail:{email}"
        if facebook:
            extra_info += f"\nFacebook:{facebook}"

        full_content = f"{content}{extra_info}"
        print(full_content)
        new_post = Post(
            post_id=str(uuid.uuid4()),
            content=full_content,
            image_url=None,  
            is_approved=True if current_user.roles == 'admin' else False,
            status='Not done',
            user_id=current_user.id,
            post_type=type_mapping.get(post_type, post_type),
            create_date=datetime.now(pytz.utc),
            approval_date=None,
            submit_date =None,
            category_id = category_id

        )

        csdl.session.add(new_post)
        csdl.session.commit()
        post_id = new_post.post_id

        # Xử lý upload ảnh sau khi có post_id
        image_urls = []
        # Thư mục lưu ảnh upload
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads')
        for index, image_file in enumerate(images):
            if image_file and allowed_file(image_file.filename):
                # Lấy đuôi file
                file_ext = image_file.filename.rsplit('.', 1)[1].lower()

                # Đặt tên file theo post_id
                if len(images) == 1:
                    filename = f"{post_id}.{file_ext}"
                else:
                    filename = f"{post_id} ({index+1}).{file_ext}"

                # Đường dẫn lưu file
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                image_file.save(save_path)

                # Thêm vào danh sách URL ảnh
                image_urls.append(f'/static/uploads/{filename}')

        # Cập nhật image_url vào bài post
        if image_urls:
            new_post.image_url = ','.join(image_urls)
            csdl.session.commit()

        flash(
            'Bài viết đã được đăng thành công!' if current_user.roles == 'admin'
            else 'Bài viết đã được gửi và đang chờ duyệt. Vui lòng đợi admin xét duyệt.',
            'success'
        )

        return redirect(url_for('post.my_posts'))

    return render_template('post/create_post.html' ,categories=categories)



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
    post.end_time = datetime.now(pytz.utc)
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

    # Xóa các ảnh trong folder nếu có
    if post.image_url:
        # Lấy đường dẫn đến thư mục uploads
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')

        # Lấy danh sách các ảnh (tách chuỗi image_url bằng dấu phẩy)
        image_urls = post.image_url.split(',')

        for url in image_urls:
            # Lấy tên file từ URL (bỏ phần '/static/uploads/' ở đầu)
            filename = url.replace('/static/uploads/', '')
            file_path = os.path.join(upload_folder, filename)

            # Kiểm tra và xóa file nếu tồn tại
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    current_app.logger.error(f"Lỗi khi xóa file {file_path}: {str(e)}")

    # Xóa bài viết từ database
    csdl.session.delete(post)
    csdl.session.commit()

    flash('Bài viết và các ảnh đính kèm đã được xóa.', 'success')
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
        # Cập nhật nội dung
        post.content = request.form['content']

        # Xử lý ảnh bị xóa
        deleted_images = request.form.get('deleted_images', '')
        if deleted_images:
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            for url in deleted_images.split(','):
                if url:  # Kiểm tra url không rỗng
                    filename = url.replace('/static/uploads/', '')
                    file_path = os.path.join(upload_folder, filename)
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            current_app.logger.error(f"Lỗi khi xóa file {file_path}: {str(e)}")

            # Cập nhật image_url (loại bỏ các ảnh đã xóa)
            if post.image_url:
                remaining_images = [url for url in post.image_url.split(',') if url not in deleted_images.split(',')]
                post.image_url = ','.join(remaining_images) if remaining_images else None

        # Xử lý ảnh mới
        new_images = request.files.getlist('images')
        if new_images and new_images[0].filename != '':
            # Upload ảnh mới
            image_urls = []
            for index, image_file in enumerate(new_images):
                if image_file and allowed_file(image_file.filename):
                    # Lấy đuôi file
                    file_ext = image_file.filename.rsplit('.', 1)[1].lower()

                    # Đặt tên file theo post_id
                    if len(new_images) == 1:
                        filename = f"{post_id}.{file_ext}"
                    else:
                        filename = f"{post_id} ({index+1}).{file_ext}"

                    # Đường dẫn lưu file
                    save_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    image_file.save(save_path)

                    # Thêm vào danh sách URL ảnh
                    image_urls.append(f'/static/uploads/{filename}')

            # Thêm ảnh mới vào image_url hiện có
            if image_urls:
                current_images = post.image_url.split(',') if post.image_url else []
                current_images.extend(image_urls)
                post.image_url = ','.join(current_images)

        csdl.session.commit()
        flash("Bài đăng đã được cập nhật.", "success")
        return redirect(url_for('post.my_posts'))

    return render_template('post/edit_post.html', post=post)


@post_blueprint.route('/remember-phone', methods=['POST'])
@login_required
def remember_phone():
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({'status': 'error', 'message': 'Phone is missing'}), 400

    current_user.phone = phone
    csdl.session.commit()
    return jsonify({'status': 'success', 'message': 'Phone updated'})
@post_blueprint.route('/remember-email', methods=['POST'])
@login_required
def remember_email():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'status': 'error', 'message': 'email is missing'}), 400

    current_user.email = email
    csdl.session.commit()
    return jsonify({'status': 'success', 'message': 'email updated'})
@post_blueprint.route('/remember-facebook', methods=['POST'])
@login_required
def remember_facebook():
    data = request.get_json()
    facebook = data.get('facebook')

    if not facebook:
        return jsonify({'status': 'error', 'message': 'facebook is missing'}), 400

    current_user.facebook = facebook
    csdl.session.commit()
    return jsonify({'status': 'success', 'message': 'facebook updated'})


def parse_contact(content):
    # Tách các dòng liên hệ sau "Liên hệ:"
    contact_data = []
    if 'Liên hệ:' not in content:
        return contact_data

    lines = content.split('Liên hệ:')[1].strip().split('\n')
    for line in lines:
        if ':' not in line:
            continue
        label, value = line.split(':', 1)
        value = value.strip()
        # Bỏ qua nếu giá trị rỗng hoặc là 'None'
        if value and value.lower() != 'none':
            contact_data.append({
                'label': label.strip().capitalize(),  # Viết hoa nhãn
                'value': value
            })
    return contact_data


@post_blueprint.route('/view_post', methods=['GET', 'POST'])
def viewPost():
    form = FilterForm()
    users = User.query.all()
    posts = Post.query.order_by(Post.create_date.desc()).all()  # mặc định ban đầu

    if form.validate_on_submit():
   
        # KHỞI TẠO query trước
        query = Post.query

        

        post_type = form.post_type.data
        sort_order = form.sort_order.data

        if post_type != 'all':
            query = query.filter(Post.post_type == post_type)

        if sort_order == 'desc':
            query = query.order_by(Post.create_date.desc())
        else:
            query = query.order_by(Post.create_date.asc())

        posts = query.all()

    # Gắn thông tin liên hệ đã tách vào mỗi post
    for post in posts:
        post.contact_info = parse_contact(post.content)

    return render_template('post/view_post.html', posts=posts, users=users, form=form)

    
    


@post_blueprint.route('/interest/<string:post_id>', methods=['POST'])
@login_required 
def add_interest(post_id):
    post = Post.query.get_or_404(post_id)
    # Lấy danh sách user_id đã quan tâm
    user_ids = post.interested_user_id.split(',') if post.interested_user_id else []

    if str(current_user.id) in user_ids:
        flash("Bạn đã quan tâm bài viết này rồi.", "warning")
    else:
        user_ids.append(str(current_user.id))
        post.interested_user_id = ','.join(user_ids)
        post.interest_count += 1
        csdl.session.commit()
        flash("Đã quan tâm bài viết.", "success")
    return redirect(url_for('post.viewPost'))