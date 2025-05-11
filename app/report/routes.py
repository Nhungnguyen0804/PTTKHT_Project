from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from . import report_blueprint
from app.models.user import User, user_role
from app.models.role import Role
from app.models.post import Post
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


