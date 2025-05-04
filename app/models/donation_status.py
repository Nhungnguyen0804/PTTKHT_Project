from app.flask_extensions import csdl, login_manager

class DonationStatus(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    category_name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...


def init_status():
    """Hàm khởi tạo các vai trò mặc định (admin và member) nếu chưa tồn tại."""
    if DonationStatus.query.count() == 0:
        pending = DonationStatus(category_name="Đang chờ duyệt")
        donated = DonationStatus(category_name="Quyên góp thành công")
        canceled = DonationStatus(category_name="Đã bị huỷ")
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