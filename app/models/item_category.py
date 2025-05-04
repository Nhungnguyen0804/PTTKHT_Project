from app.flask_extensions import csdl, login_manager

class ItemCategory(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    category_name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...


def init_categories():
    """Hàm khởi tạo các vai trò mặc định (admin và member) nếu chưa tồn tại."""
    if ItemCategory.query.count() == 0:
        money = ItemCategory(category_name="Tiền")
        learning_supply = ItemCategory(category_name="Dụng cụ học tập")
        clothes = ItemCategory(category_name="Quần áo")
        bicycle = ItemCategory(category_name="Xe đạp")
        csdl.session.add(money)
        csdl.session.add(learning_supply)
        csdl.session.add(clothes)
        csdl.session.add(bicycle)
        try:
            csdl.session.commit()
            print("Đã thêm các loại đồ quyên góp")
        except Exception as e:
            csdl.session.rollback()
            print(f"Lỗi khi thêm vai trò: {e}")
    else:
        print("Bảng Item Catefory đã có dữ liệu, bỏ qua khởi tạo.")