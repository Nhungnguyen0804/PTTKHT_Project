from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user

from app.models.donation import Donation
from app.models.donation_category import DonationCategory
from app.models.event import Event
from . import eventReport_blueprint
from app.models.user import User, user_role
from app.models.role import Role
from app.models.post import Post
from app.flask_extensions import csdl
from datetime import datetime
from sqlalchemy import extract, func
from .form import YearForm
from app.models.donation_item import DonationItem
from app.models.buyable_item import BuyableItem

@eventReport_blueprint.route("/report/event_report", methods=['GET', 'POST'])
def show_eventReport():
    user = csdl.session.get(User, current_user.id)
    
    # Thống kê số lượng sự kiện
    total_events = Event.query.count()

    # Lấy ngày tháng hiện tại 
    now = datetime.now()

    # Sự kiện mới trong ngày
    start_today = datetime(now.year, now.month, now.day)  # 0h hôm nay
    new_event_today = Event.query.filter(Event.start_time >= start_today).all()
    new_event_today_count = len(new_event_today)

    # Sự kiện mới trong tháng này
    new_event_month = Event.query.filter(
        extract('month', Event.start_time) == now.month,
        extract('year', Event.start_time) == now.year).all()
    new_event_month_count = len(new_event_month)

    # Sự kiện mới trong năm nay
    new_event_year = Event.query.filter(
        extract('year', Event.start_time) == now.year
    ).all()
    new_event_year_count = len(new_event_year)

    # Biểu đồ thống kê
    form = YearForm()
    # Lấy năm được chọn từ form (hoặc mặc định là năm hiện tại)
    selected_year = form.year.data if form.validate_on_submit() else datetime.now().year
    
    # Lấy tháng hiện tại
    current_month = datetime.now().month

    # Tính số lượng sự kiện theo từng tháng cho năm được chọn
    event_counts = [0] * 12  # Mảng chứa số lượng sự kiện cho từng tháng (1-12)
    for month in range(1, current_month + 1):
        # Truy vấn số sự kiện trong tháng và năm được chọn
        count = Event.query.filter(extract('year', Event.start_time) == selected_year, 
                                   extract('month', Event.start_time) == month).count()
        event_counts[month - 1] = count
    
    # Cắt event_counts đến tháng hiện tại
    event_counts = event_counts[:current_month]

    # Điền các tháng còn lại bằng 0 để khớp với 12 nhãn
    event_counts.extend([0] * (12 - len(event_counts)))

    # Thống kê số lượng sự kiện theo loại (Event Type)
    event_type_counts = {}
    for event_type in Event.query.with_entities(Event.event_type).distinct():
        event_type_count = Event.query.filter(Event.event_type == event_type[0]).count()
        event_type_counts[event_type[0]] = event_type_count

    # Top sự kiện theo loại
    event_type = request.args.get("type", "Thanh Lý")  # default là "Thanh Lý"
    top_events = (
        csdl.session.query(
            Event.name,
            Event.start_time,
            func.count(Donation.id).label("donation_count")
        )
        .join(DonationCategory, DonationCategory.event_id == Event.id)
        .join(Donation, Donation.donation_category_id == DonationCategory.id)
        .group_by(Event.id, Event.name, Event.start_time)
        .having(func.count(Donation.id) > 0)
        .order_by(func.count(Donation.id).desc())
        .limit(5)
        .all()
    )

    # Thống kê số vật phẩm đã nhận và số tiền đã bán cho từng sự kiện
    events = Event.query.all()
    event_reports = []
    for event in events:
        # Số vật phẩm đã nhận
        received_item_count = (
            csdl.session.query(DonationItem)
            .join(DonationCategory, DonationItem.category_id == DonationCategory.id)
            .filter(DonationCategory.event_id == event.id)
            .count()
        )
        # Số tiền đã bán
        sold_amount = (
            csdl.session.query(func.coalesce(func.sum(BuyableItem.price), 0))
            .filter(BuyableItem.event_id == event.id, BuyableItem.status == 'Đã bán')
            .scalar()
        )
        event_reports.append({
            "id": event.id,
            "name": event.name,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "event_type": event.event_type,
            "managed_by": event.managed_by if hasattr(event, "managed_by") else [],
            "received_item_count": received_item_count,
            "sold_amount": sold_amount
        })

    return render_template(
        'eventReport/eventReport.html.jinja2',
        user=user,
        total_events=total_events, 
        new_event_today_count=new_event_today_count, 
        new_event_month_count=new_event_month_count,
        new_event_year_count=new_event_year_count,
        event_counts=event_counts,
        form=form,
        event_type_counts=event_type_counts,
        top_events=top_events, 
        selected_event_type=event_type,
        events=event_reports  # Truyền danh sách sự kiện kèm thống kê sang template
    )