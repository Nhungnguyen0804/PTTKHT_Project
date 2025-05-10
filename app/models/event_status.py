from app.flask_extensions import csdl, login_manager

class EventStatus(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...


def init_estatus():
    if EventStatus.query.count() == 0:
        running = EventStatus(name="Đang triển khai")
        postponed = EventStatus(name="Tạm hoãn")
        canceled = EventStatus(name="Đã bị huỷ")
        csdl.session.add(running)
        csdl.session.add(postponed)
        csdl.session.add(canceled)
        try:
            csdl.session.commit()
            print("Đã thêm các loại đồ quyên góp")
        except Exception as e:
            csdl.session.rollback()
            print(f"Lỗi khi thêm vai trò: {e}")
    else:
        print("Bảng Item Catefory đã có dữ liệu, bỏ qua khởi tạo.")