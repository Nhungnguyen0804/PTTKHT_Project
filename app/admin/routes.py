from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app
from app.admin.forms import EventAdderForm, DonationCategoryAdderForm, BuyableItemForm
from app.models.buyable_item import BuyableItem
from app.models.donation import Donation
from app.models.donation_item import DonationItem
from app.models.event import Event
from app.models.donation_category import DonationCategory
from app.flask_extensions import csdl
from sqlalchemy.orm import joinedload

admin_blueprint = Blueprint('admin', __name__,template_folder='templates')


@admin_blueprint.route('/admin')
def adminPage():
    events = current_user.managed_events
    return render_template('admin/adminDashboard.html', events=events)

@admin_blueprint.route('/admin/event', methods=['GET', 'POST'])
@admin_blueprint.route('/admin/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def manageEvent(event_id=None):
    print(f"[DEBUG] Current request URL: {request.url}")

    event = Event.query.get(event_id) if event_id else None
    form = EventAdderForm(obj=event)

    if event and event.status_id == 3:
        flash("Không thể chuyển sự kiện sang trạng thái 'Huỷ'.", "warning")
        return redirect(request.referrer or url_for('admin.adminPage'))

    now = datetime.utcnow()

    if request.method == 'GET' and event:
        form.startTime.data = event.start_time.replace(microsecond=0)
        form.endTime.data = event.end_time.replace(microsecond=0)

    if form.validate_on_submit():
        image_file = form.image.data
        image_path = event.image if event else None

        # Nếu người dùng upload ảnh mới
        if image_file and hasattr(image_file, 'filename') and image_file.filename:
            filename = secure_filename(image_file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join('uploads', filename).replace('\\', '/')
            image_file.save(os.path.join(upload_folder, filename))
        elif not event:
            flash("Vui lòng tải lên ảnh cho sự kiện mới.", "danger")
            return render_template('admin/addEvent.html', form=form, event=event, now=now)

        # Nếu đang sửa
        if event:
            # Kiểm tra nếu startTime cũ < hiện tại và form.startTime mới > hiện tại => không hợp lệ
            if event.start_time < now and form.startTime.data > now:
                flash("Không thể thay đổi thời gian bắt đầu từ quá khứ sang tương lai.", "danger")
                return render_template('admin/addEvent.html', form=form, event=event, now=now)

            if form.startTime.data >= form.endTime.data:
                flash("Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc!", "danger")
                return render_template('admin/addEvent.html', form=form, event=event, now=now)

            event.name = form.name.data
            event.start_time = form.startTime.data
            event.end_time = form.endTime.data
            event.event_type = form.eventType.data
            event.image = image_path

            csdl.session.commit()
            flash('Đã cập nhật sự kiện.', 'success')
        else:
            if form.startTime.data >= form.endTime.data:
                flash("Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc!", "danger")
                return render_template('admin/addEvent.html', form=form, now=now)

            event = Event(
                name=form.name.data,
                start_time=form.startTime.data,
                end_time=form.endTime.data,
                event_type=form.eventType.data,
                status_id=1,
                image=image_path
            )
            event.managed_by.append(current_user)
            csdl.session.add(event)
            csdl.session.commit()
            flash("Thêm sự kiện thành công!", "success")

        return redirect(url_for('admin.adminPage'))

    return render_template('admin/addEvent.html', form=form, event=event, now=now)



@admin_blueprint.route('/admin/<int:event_id>')
def showEventDetails(event_id):
    event = Event.query.get(event_id)

    if event and event.status_id == 3:
        flash("Không thể chuyển sự kiện sang trạng thái 'Huỷ'.", "warning")
        return redirect(request.referrer or url_for('admin.adminPage'))

    if event:
        # Lấy tất cả donation_category_id của sự kiện
        category_ids = [dc.id for dc in event.donation_categories]

        # Truy vấn tất cả Donation thuộc các category đó
        donations = Donation.query.filter(Donation.donation_category_id.in_(category_ids)).all()

        return render_template(
            'admin/eventDetails.html',
            event=event,
            donations=donations,
            now=datetime.utcnow()
        )
    else:
        flash("Không tìm thấy sự kiện.", "danger")
        return redirect(url_for('admin.adminPage'))


    
@admin_blueprint.route('/admin/<int:event_id>/dc', methods=['GET', 'POST'])
@admin_blueprint.route('/admin/<int:event_id>/dc/<int:donation_category_id>', methods=['GET', 'POST'])
def manageDonationCategory(event_id, donation_category_id=None):
    event = Event.query.get(event_id)
    donation_category = DonationCategory.query.get(donation_category_id) if donation_category_id else None
    form = DonationCategoryAdderForm(obj=donation_category)
    if event and event.status_id == 3:
        flash("Không thể chuyển sự kiện sang trạng thái 'Huỷ'.", "warning")
        return redirect(request.referrer or url_for('admin.adminPage'))
    # Gán giá trị datetime khi đang GET (hiển thị form với dữ liệu cũ)
    if request.method == 'GET' and donation_category:
        form.startDate.data = event.start_date.replace(microsecond=0)
        form.endDate.data = event.end_date.replace(microsecond=0)

    if form.validate_on_submit():
        if donation_category:
            form.populate_obj(donation_category)
            csdl.session.commit()
            flash('Đã cập nhật hạng mục quyên góp.', 'success')
        else:
            # Kiểm tra logic start < end
            if form.startDate.data >= form.endDate.data:
                flash("Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc!", "danger")
                return render_template('admin/addDonationCategory.html', form=form)

            # Tạo đối tượng sự kiện mới
            donation_category = DonationCategory(
                dc_name=form.name.data,
                donation_type = form.donationType.data,
                target_quantity = form.targetQuantity.data,
                start_date = form.startDate.data,
                end_date = form.endDate.data,
                dc_type_id = form.dcType.data,
                event_id = event_id,
                status_id = 1
            )
            
            csdl.session.add(donation_category)
            csdl.session.commit()
            flash("Thêm sự kiện thành công!", "success")
        

        return redirect(url_for('admin.adminPage'))

    return render_template('admin/addDonationCategory.html', form=form)

@admin_blueprint.route("/admin/<int:category_id>/details", methods=["POST", "GET"])
def manageDonationCategories(category_id):
    category = DonationCategory.query.get(category_id)
    
    # list of donations from category here
    donations_of_category = Donation.query.options(
    joinedload(Donation.items),
    joinedload(Donation.status)
).filter_by(donation_category_id=category.id).all()
    return render_template("admin/donationCategoryDetails.html", category=category, donations_of_category=donations_of_category)

@admin_blueprint.route('/admin/confirm_donation/<int:donation_id>', methods=['POST'])
@login_required
def confirm_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    
    # Giả sử 2 là trạng thái "Đã xác nhận"
    donation.status_id = 2
    csdl.session.commit()

    dc = DonationCategory.query.get(donation.donation_category_id)
    if dc.dc_type_id == 3:
        # Truyền theo event_id và donation_item.id đầu tiên (ví dụ: chỉ xử lý 1 item)
        if donation.items:
            donation_item_id = donation.items[0].id
            return redirect(url_for('admin.createBuyableItem',
                                    event_id=dc.event_id,
                                    donation_item_id=donation_item_id))
        else:
            flash("Không tìm thấy vật phẩm quyên góp để chuyển thành sản phẩm trao đổi.", "warning")
            return redirect(request.referrer or url_for('admin.manageDonationCategories', category_id=dc.id))

    flash("Đã xác nhận lượt quyên góp.", "success")
    return redirect(request.referrer or url_for('admin.manageDonationCategories', category_id=dc.id))

@admin_blueprint.route('/admin/cancel_donation/<int:donation_id>', methods=['POST'])
@login_required
def cancel_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    # Giả sử 3 là trạng thái "Đã hủy"
    donation.status_id = 3
    csdl.session.commit()
    flash("Đã hủy lượt quyên góp.", "warning")
    return redirect(request.referrer or url_for('admin.manageDonationCategories', category_id=donation.donation_category_id))

@admin_blueprint.route('/<int:event_id>/<int:donation_item_id>/buyable', methods=['GET', 'POST'])
@admin_blueprint.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def createBuyableItem(event_id=None, donation_item_id=None, item_id=None):
    form = BuyableItemForm()
    event = Event.query.get(event_id)
    if event and event.status_id == 3:
        flash("Không thể chuyển sự kiện sang trạng thái 'Huỷ'.", "warning")
        return redirect(request.referrer or url_for('admin.adminPage'))
    if item_id:  # Trường hợp chỉnh sửa
        item = BuyableItem.query.get_or_404(item_id)
        if request.method == 'GET':
            form.item_name.data = item.item_name
            form.price.data = item.price
        if form.validate_on_submit():
            image_file = form.image.data
            if image_file:
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join('uploads', filename).replace("\\", "/")
                image_file.save(os.path.join(upload_folder, filename))
                item.image = image_path  # Cập nhật ảnh mới nếu có

            item.item_name = form.item_name.data
            item.price = form.price.data
            csdl.session.commit()
            flash("Đã cập nhật Buyable Item thành công.", "success")
            return redirect(url_for('admin.adminPage'))

        return render_template("admin/addBuyableItem.html", form=form, item=item)

    else:  # Trường hợp tạo mới từ DonationItem
        donation_item = DonationItem.query.get_or_404(donation_item_id)
        if request.method == 'GET':
            form.item_name.data = donation_item.item_name

        if form.validate_on_submit():
            image_file = form.image.data
            image_path = None
            if image_file:
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join('uploads', filename).replace("\\", "/")
                image_file.save(os.path.join(upload_folder, filename))

            new_item = BuyableItem(
                event_id=event_id,
                item_name=form.item_name.data,
                price=form.price.data,
                image=image_path or donation_item.image,
                item_category_id=donation_item.category_id,
                status=1  # mặc định active
            )
            csdl.session.add(new_item)
            csdl.session.commit()
            flash("Đã tạo Buyable Item thành công.", "success")
            return redirect(url_for('admin.adminPage'))

        return render_template("admin/addBuyableItem.html", form=form, event_id=event_id, donation_item=donation_item)

@admin_blueprint.route('/buyable_item/<int:item_id>/status/<int:new_status>')
def updateBuyableItemStatus(item_id, new_status):
    item = BuyableItem.query.get_or_404(item_id)

    if new_status not in [2, 3]:
        flash("Trạng thái không hợp lệ.", "danger")
        return redirect(request.referrer or url_for('admin.adminPage'))

    item.status = new_status
    csdl.session.commit()
    flash(f"Đã cập nhật trạng thái '{item.item_name}' thành {new_status}.", "success")
    return redirect(request.referrer or url_for('admin.adminPage'))

@admin_blueprint.route('/<int:event_id>/<int:status_id>')
def updateEventStatus(event_id, status_id):  
    event = Event.query.get(event_id)
    if event and event.status_id == 3:
        flash("Không thể chuyển sự kiện sang trạng thái 'Huỷ'.", "warning")
        return redirect(request.referrer or url_for('admin.adminPage'))
    event = Event.query.get(event_id)
    event.status_id = status_id
    csdl.session.commit()
    return redirect(request.referrer or url_for('admin.adminPage'))

@admin_blueprint.route('/donation-category/<int:category_id>/pause')
def pause_donation_category(category_id):
    dc = DonationCategory.query.get_or_404(category_id)
    if dc.status_id == 3:
        flash('Không thể tạm dừng hạng mục đã huỷ.', 'danger')
    else:
        dc.status_id = 2  # ID trạng thái "tạm hoãn"
        csdl.session.commit()
        flash('Hạng mục đã được tạm dừng.', 'success')
    return redirect(url_for('admin.showEventDetails', event_id=dc.event_id))


@admin_blueprint.route('/donation-category/<int:category_id>/cancel')
def cancel_donation_category(category_id):
    dc = DonationCategory.query.get_or_404(category_id)
    if dc.status_id == 3:
        flash('Hạng mục này đã bị huỷ trước đó.', 'warning')
    else:
        dc.status_id = 3  # ID trạng thái "huỷ"
        csdl.session.commit()
        flash('Hạng mục đã được huỷ.', 'success')
    return redirect(url_for('admin.showEventDetails', event_id=dc.event_id))


@admin_blueprint.route('/donation-category/<int:category_id>/resume')
def resume_donation_category(category_id):
    category = DonationCategory.query.get_or_404(category_id)
    category.status_id = 1  # trạng thái "Đang hoạt động"
    csdl.session.commit()
    flash("Hạng mục quyên góp đã được tiếp tục.", "success")
    return redirect(request.referrer or url_for('admin.adminPage'))