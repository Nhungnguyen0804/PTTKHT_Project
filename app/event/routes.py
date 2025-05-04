from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user
from app.flask_extensions import csdl
from app.event.forms import ItemDonationForm, MoneyDonationForm
from app.models.donation import Donation
from app.models.donation_category import DonationCategory
from app.models.donation_item import DonationItem
from app.models.event import Event
from app.models.item_category import ItemCategory
event_blueprint = Blueprint('event', __name__,template_folder='templates')

@event_blueprint.route('/event')
def event():
    events = Event.query.all()

    # Gắn trường donationCategories cho mỗi event
    for e in events:
        # Lấy danh sách tên hạng mục quyên góp
        category_names = [cat.dc_name for cat in e.donation_categories]
        # Gộp thành chuỗi ngăn cách bằng dấu phẩy
        e.donationCategories = ", ".join(category_names)
        e.donationCategoryCount = e.donation_categories.count()

    return render_template('event/event.html', events=events)

@event_blueprint.route('/<int:category_id>/details', methods=["GET", "POST"])
def addDonation(category_id):
    category = DonationCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        # Tạo mới một Donation
        new_donation = Donation(
            donation_category_id=category.id,
            donor_name=current_user.username,
            donor_email=current_user.email,
            create_time=datetime.utcnow()
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
                item_category_id=item_data['item_category_id'],
                donation_id=new_donation.id
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
@event_blueprint.route('/<int:category_id>/<int:item_number>', methods=['GET', 'POST'])
def manageDonationItem(category_id, item_number=None):
    category = DonationCategory.query.get_or_404(category_id)
    donation_items = session.get('donation_items', [])

    # Dữ liệu item nếu đang sửa
    donation_data = donation_items[item_number] if item_number is not None and item_number < len(donation_items) else None

    # Chọn form
    if category.donation_type == "money":
        form = MoneyDonationForm(data=donation_data)
    else:
        form = ItemDonationForm(data=donation_data)
        
        # Lấy danh sách loại sản phẩm và gán vào form
        categories = ItemCategory.query.all()
        form.itemCategoryId.choices = [(c.id, c.category_name) for c in categories]

    if form.validate_on_submit():
        if category.donation_type == "money":
            new_item = {
                'item_name': f"Quyên góp tiền cho hạng mục {category.dc_name}",
                'quantity': form.quantity.data,
                'item_category_id': 1  # hoặc None
            }
        else:
            new_item = {
                'item_name': form.itemName.data,
                'quantity': form.quantity.data,
                'item_category_id': form.itemCategoryId.data
            }

        # Ghi đè nếu đang sửa, thêm mới nếu không
        if item_number is not None and item_number < len(donation_items):
            donation_items[item_number] = new_item
        else:
            donation_items.append(new_item)

        session['donation_items'] = donation_items
        flash("Thêm/Chỉnh sửa vật phẩm thành công", "success")
        return redirect(url_for('event.addDonation', category_id=category_id))

    return render_template('event/addDonationItem.html', form=form, category=category)


