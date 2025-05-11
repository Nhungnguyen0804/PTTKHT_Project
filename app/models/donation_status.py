from app.flask_extensions import csdl, login_manager

class DonationStatus(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...


def init_status():
    if DonationStatus.query.count() == 0:
        pending = DonationStatus(name="Đang chờ duyệt")
        donated = DonationStatus(name="Quyên góp thành công")
        canceled = DonationStatus(name="Đã bị huỷ")
        csdl.session.add(pending)
        csdl.session.add(donated)
        csdl.session.add(canceled)
        try:
            csdl.session.commit()
            print("Đã thêm các loại đồ quyên góp")
        except Exception as e:
            csdl.session.rollback()
            print(f"Lỗi khi thêm vai trò: {e}")
    else:
        print("Bảng Item Catefory đã có dữ liệu, bỏ qua khởi tạo.")