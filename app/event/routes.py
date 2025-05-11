from datetime import datetime
import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from app.flask_extensions import csdl
from werkzeug.utils import secure_filename
from flask import current_app
from app.event.forms import ItemDonationForm, MoneyDonationForm
from app.models.donation import Donation
from app.models.donation_category import DonationCategory
from app.models.donation_item import DonationItem
from app.models.event import Event
from app.models.item_category import Category
from app.models.user import User
event_blueprint = Blueprint('event', __name__,template_folder='templates')

@event_blueprint.route('/event/', defaults={'user_id': None})
@event_blueprint.route('/event/<int:user_id>')
def event(user_id):
    from sqlalchemy.orm import joinedload

    if user_id is None:
        # Trường hợp không có user_id → hiển thị tất cả sự kiện
        events = Event.query.options(joinedload(Event.donation_categories)).all()
    else:
        # Trường hợp có user_id → lọc các event mà user đã quyên góp
        user = User.query.get_or_404(user_id)

        donations = Donation.query.filter(
            (Donation.donor_email == user.email) |
            (Donation.donor_name == user.username)
        ).all()

        category_ids = [donation.donation_category_id for donation in donations if donation.donation_category_id]

        # Truy vấn các event_id tương ứng
        event_ids = {
            dc.event_id for dc in DonationCategory.query.filter(DonationCategory.id.in_(category_ids)).all()
        }

        events = Event.query.options(joinedload(Event.donation_categories)) \
            .filter(Event.id.in_(event_ids)).all()

    # Gắn thêm thông tin hạng mục
    for e in events:
        category_names = [cat.dc_name for cat in e.donation_categories]
        e.donationCategories = ", ".join(category_names)
        e.donationCategoryCount = len(e.donation_categories)

    return render_template('event/event.html', events=events, now=datetime.utcnow())


@event_blueprint.route('/<int:category_id>/details', methods=["GET", "POST"])
def manageDonation(category_id):
    category = DonationCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        # Tạo mới một Donation
        new_donation = Donation(
            donation_category_id=category.id,
            donor_name=current_user.username,
            donor_email=current_user.email,
            create_time=datetime.utcnow(),
            status_id = 1
        )
        csdl.session.add(new_donation)
        csdl.session.commit()  # Cần commit để có được ID

        # Lấy danh sách các item từ session
        donation_items_data = session.pop('donation_items', [])

        # Tạo các DonationItem tương ứng
        for item_data in donation_items_data:
            donation_item = DonationItem(
                item_name=item_data['item_name'],
                quantity=item_data['quantity'],
                category_id=item_data['category_id'],
                donation_id=new_donation.id,
                image = item_data['image_url']
            )
            csdl.session.add(donation_item)

        csdl.session.commit()

        flash("Đăng ký quyên góp thành công!", "success")
        return redirect(url_for('event.event'))

    # Nếu là GET, hiển thị danh sách tạm
    donation_items = session.get('donation_items', [])
    return render_template("event/addDonation.html", category=category, donation_items=donation_items)


@event_blueprint.route('/<int:category_id>/additem', methods=['GET', 'POST'])
@event_blueprint.route('/<int:category_id>/<int:item_id>', methods=['GET', 'POST'])
@event_blueprint.route('/<int:category_id>/items/<int:item_number>', methods=['GET', 'POST'])
def manageDonationItem(category_id, item_number=None):
    category = DonationCategory.query.get_or_404(category_id)
    donation_items = session.get('donation_items', [])
    donation_data = donation_items[item_number] if item_number is not None and item_number < len(donation_items) else None

    form = MoneyDonationForm(data=donation_data) if category.donation_type == "money" else ItemDonationForm(data=donation_data)

    if category.donation_type != "money":
        categories = Category.query.all()
        form.itemCategoryId.choices = [(c.id, c.category_name) for c in categories]
    if donation_data:
        form.itemName.data = donation_data['item_name']
        form.quantity.data = donation_data['quantity']
        form.itemCategoryId.data = donation_data['category_id']
    if form.validate_on_submit():
        image_url = None
        if category.donation_type != "money" and form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            image_file.save(upload_path)
            image_url = f'static/uploads/{filename}'

        if category.donation_type == "money":
            new_item = {
                'item_name': f"Quyên góp tiền cho hạng mục {category.dc_name}",
                'quantity': form.quantity.data,
                'category_id': 24,
            }
        else:
            new_item = {
                'item_name': form.itemName.data,
                'quantity': form.quantity.data,
                'category_id': form.itemCategoryId.data,
                'image_url': image_url
            }

        if item_number is not None and item_number < len(donation_items):
            donation_items[item_number] = new_item
        else:
            donation_items.append(new_item)

        session['donation_items'] = donation_items
        flash("Thêm/Chỉnh sửa vật phẩm thành công", "success")
        return redirect(url_for('event.manageDonation', category_id=category_id))

    return render_template('event/addDonationItem.html', form=form, category=category)

@event_blueprint.route('/<int:event_id>/donations')
@login_required
def displayAllDonations(event_id):
    event = Event.query.get_or_404(event_id)
    categories = DonationCategory.query.filter_by(event_id=event_id).all()

    donation_map = {}
    for cat in categories:
        donations = Donation.query.filter_by(
            donation_category_id=cat.id,
            donor_email=current_user.email
        ).all()
        donation_map[cat.id] = donations

    return render_template(
        'event/displayDonation.html',
        event=event,
        categories=categories,
        donation_map=donation_map
    )
