from app.flask_extensions import csdl, login_manager

class Role(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    name = csdl.Column(csdl.String(50), unique=True, nullable=False)  # Tên vai trò: 'admin', 'user', ...


def init_roles():
    """Hàm khởi tạo các vai trò mặc định (admin và member) nếu chưa tồn tại."""
    if Role.query.count() == 0:
        admin_role = Role(id=1, name='admin')
        member_role = Role(id=2, name='member')
        csdl.session.add(admin_role)
        csdl.session.add(member_role)
        try:
            csdl.session.commit()
            print("Đã thêm các vai trò mặc định: admin, member")
        except Exception as e:
            csdl.session.rollback()
            print(f"Lỗi khi thêm vai trò: {e}")
    else:
        print("Bảng Role đã có dữ liệu, bỏ qua khởi tạo.")