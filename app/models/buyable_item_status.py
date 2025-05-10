from app.flask_extensions import csdl, login_manager

class BuyableItemStatus(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...


def init_status():
    if BuyableItemStatus.query.count() == 0:
        avaliable = BuyableItemStatus(name="Còn hàng")
        sold = BuyableItemStatus(name="Đã được mua")
        canceled = BuyableItemStatus(name="Đã bị huỷ")
        csdl.session.add(avaliable)
        csdl.session.add(sold)
        csdl.session.add(canceled)
        try:
            csdl.session.commit()
            print("Đã thêm các loại đồ quyên góp")
        except Exception as e:
            csdl.session.rollback()
            print(f"Lỗi khi thêm vai trò: {e}")
    else:
        print("Bảng Item Catefory đã có dữ liệu, bỏ qua khởi tạo.")