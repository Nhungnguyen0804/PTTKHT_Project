from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from . import report_blueprint
from app.models.user import User, user_role
from app.models.role import Role
from app.models.post import Post
from app.models.category import Category
from app.flask_extensions import csdl
from datetime import datetime
from sqlalchemy import extract
from .form import YearForm
from sqlalchemy import func


@report_blueprint.route("/report/user_report" ,methods=['GET', 'POST'])
def show_userReport():
    user = csdl.session.get(User, current_user.id)
    # thong ke so luong user
    total_users = User.query.count()
    print(total_users)

    #lấy ngày tháng hiện tại 
    now = datetime.now()

    
    # user moi trong ngay 
    start_today = datetime(now.year, now.month, now.day) # 0h today
    new_user_today = User.query.filter(User.created_date >= start_today).all()
    new_user_today_count = len(new_user_today)

    new_user_month = User.query.filter(
    extract('month', User.created_date) == now.month,
    extract('year', User.created_date) == now.year).all()
    new_user_month_count = len(new_user_month)

    new_user_year = User.query.filter(
        extract('year', User.created_date) == now.year
    ).all()

    new_user_year_count = len(new_user_year)

    # bar chart 
    form = YearForm()
    
    # Lấy năm được chọn từ form (hoặc mặc định là năm hiện tại)
    selected_year = form.year.data if form.validate_on_submit() else now.year

    if form.validate_on_submit(): # Chỉ True nếu là POST và dữ liệu hợp lệ
        selected_year = form.year.data # form.year.data đã là int do coerce=int
        # form.year.data đã chứa giá trị người dùng chọn, template sẽ hiển thị đúng
    else: # Đây là GET request hoặc POST request nhưng validation thất bại
        print("Form validation GET request.")
        if request.method == 'GET': # GET request
            # Đặt giá trị mặc định cho SelectField để hiển thị đúng năm hiện tại
            form.year.data = now.year
          


    print(form.validate_on_submit())
    print(selected_year)
    #lay thang hien tai
    current_month = now.month
    current_year = now.year

    # Tính số lượng người dùng đăng ký theo từng tháng cho năm được chọn
    user_counts = [0] * 12  # Mảng chứa số lượng người dùng cho từng tháng (1-12)
    for month in range(1, 13):
        # Nếu đang xét năm hiện tại và vượt quá tháng hiện tại thì dừng
        if selected_year == current_year and month > current_month:
            break
        # Truy vấn số người dùng đăng ký trong tháng và năm được chọn
        count = User.query.filter(csdl.extract('year', User.created_date) == selected_year, 
                                  csdl.extract('month', User.created_date) == month).count()
        user_counts[month - 1] = count
    
    

    # Điền các tháng còn lại bằng 0 để khớp với 12 nhãn
    user_counts.extend([0] * (12 - len(user_counts)))
    print(user_counts)

    # kiểu user
    # Đếm học sinh (username 'hs')
    hs_count = User.query.filter(User.username.like("hs%")).count()

    # Đếm giáo viên (username 'gv')
    gv_count = User.query.filter(User.username.like("gv%")).count()

    data = {
        "label_type": ["Học sinh", "Giáo viên"],
        "count_type": [hs_count, gv_count]
    }

    # top thanh ly , dong gop, donate
    post_type = request.args.get("type", "Thanh Lý")  # default thanh ly

    top_users = (
        csdl.session.query(User.username, User.fullname, func.count(Post.post_id).label("post_count"))
        .join(Post)
        .filter(Post.post_type == post_type)
        .group_by(User.id)
        .order_by(func.count(Post.post_id).desc())
        .limit(5)
        .all()
    )

    return render_template('report/userReport.html.jinja2', 
                           user = user,
                           total_users = total_users, 
                           new_user_today_count=new_user_today_count, 
                           new_user_month_count=new_user_month_count,
                           new_user_year_count=new_user_year_count,
                           user_counts=user_counts,
                           form = form,
                           data = data,
                           top_users=top_users, 
                           selected_post_type=post_type
                           )





@report_blueprint.route("/report/post_report" ,methods=['GET', 'POST'])
# @login_required
def show_reportReport():
    csdl.session.expire_all()

    users = User.query.all()
    posts = Post.query.all()
    # thong ke so luong 
    total_post =  Post.query.count()
    

    #lấy ngày tháng hiện tại 
    now = datetime.now()

    
    # post moi trong ngay 
    start_today = datetime(now.year, now.month, now.day) # 0h today
    new_post_today = Post.query.filter(Post.create_date >= start_today).all()
    new_post_today_count = len(new_post_today)

    new_post_month = Post.query.filter(
    extract('month', Post.create_date) == now.month,
    extract('year', Post.create_date) == now.year).all()
    new_post_month_count = len(new_post_month)

    new_post_year = Post.query.filter(
        extract('year', Post.create_date) == now.year
    ).all()

    new_post_year_count = len(new_post_year)

    # bar chart 
    form = YearForm()
    # Lấy năm được chọn từ form (hoặc mặc định là năm hiện tại)
    selected_year = form.year.data if form.validate_on_submit() else now.year
    
    #lay thang hien tai
    current_month = now.month
    current_year = now.year

    # Tính số lượng từng tháng cho năm được chọn
    post_counts = [0] * 12  # Mảng chứa số lượng người dùng cho từng tháng (1-12)
    for month in range(1, 13):
        # Nếu đang xét năm hiện tại và vượt quá tháng hiện tại thì dừng
        if selected_year == current_year and month > current_month:
            break
        # Truy vấn số người dùng đăng ký trong tháng và năm được chọn
        count = Post.query.filter(csdl.extract('year', Post.create_date) == selected_year, 
                                  csdl.extract('month', Post.create_date) == month).count()
        post_counts[month - 1] = count
    
    

    # Điền các tháng còn lại bằng 0 để khớp với 12 nhãn
    post_counts.extend([0] * (12 - len(post_counts)))
    print(post_counts)


    # đếm số post chưa duyệt
    count_chua_duyet = Post.query.filter(Post.is_approved == 0).count()

    # số post đã duyệt
    count_duyet = total_post - count_chua_duyet

    data = {
        "label_type": [ "Đã Duyệt","Chưa Duyệt"],
        "count_type": [count_chua_duyet, count_duyet]
    }


    count_xong = Post.query.filter(Post.status == 'Done').count()
    count_chua_xong = total_post - count_xong
    data1 = {
        "label_type": ["Chưa Xong", "Đã Xong"],
        "count_type": [count_chua_xong, count_xong]
    }

    count_tly = Post.query.filter(Post.post_type == 'Thanh Lý').count()
    count_tdoi = Post.query.filter(Post.post_type == 'Trao Đổi').count()
    count_donate = total_post - count_xong
    dataType = {
        "label_type": ["Thanh Lý", "Trao Đổi","Đóng góp" ],
        "count_type": [count_tly, count_tdoi,count_donate]
    }

    total_care = (
    csdl.session.query(func.sum(Post.interest_count))
    .filter(extract('year', Post.create_date) == selected_year)
    .scalar()
    )


    # top thanh ly , dong gop, donate
    post_type = request.args.get("type", "Thanh Lý")  # default thanh ly

    top_users = (
        csdl.session.query(User.username, User.fullname, func.count(Post.post_id).label("post_count"))
        .join(Post)
        .filter(Post.post_type == post_type)
        .group_by(User.id)
        .order_by(func.count(Post.post_id).desc())
        .limit(5)
        .all()
    
    )

    top_posts = (
        csdl.session.query(
            Post.post_id,
            Category.category_name,
            User.fullname.label("fullname"), 
            Post.interest_count
            
        )
        .join(User, Post.user_id == User.id)
        .join(Category, Post.category_id == Category.id)
        .filter(Post.post_type == post_type)
        .group_by(Post.post_id)
        .order_by(Post.interest_count.desc())
        .limit(5)
        .all()
    )
    print(f"Đang lọc theo post_type: {post_type}")
    
    # Lấy tất cả danh mục
    categories = Category.query.all()

    # Tạo mảng lưu số lượng bài viết theo từng danh mục
    category_counts = []

    for category in categories:
        count = Post.query.filter(Post.category_id == category.id).count()
        category_counts.append(count)
    print(category_counts)
    
    category_labels = [category.category_name for category in categories]

    return render_template('report/postReport.html.jinja2', 
                           users = users, posts = posts,
                           total_post = total_post, 
                           new_post_today_count=new_post_today_count, 
                           new_post_month_count=new_post_month_count,
                           new_post_year_count=new_post_year_count,
                           post_counts=post_counts,
                           form = form, data=data, data1=data1,dataType = dataType, total_care = total_care,
                           top_users=top_users, 
                           selected_post_type=post_type, top_posts = top_posts,category_labels=category_labels ,  category_counts = category_counts
                           
                           )






