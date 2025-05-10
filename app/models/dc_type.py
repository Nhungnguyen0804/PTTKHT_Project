from app.flask_extensions import csdl

class DCType(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    type = csdl.Column(csdl.String(50), nullable=False)
    
    # Quan hệ ngược: Một DCType có nhiều DonationCategory
    categories = csdl.relationship('DonationCategory', backref='dc_type_obj', lazy=True)
    
def init_dc_types():
    """Hàm khởi tạo các loại hình quyên góp mặc định nếu chưa tồn tại."""
    from app.models.dc_type import DCType   
    if DCType.query.count() == 0:
        donate_type = DCType(type='quyên góp')
        exchange_type = DCType(type='trao đổi')
        donate_to_sell = DCType(type='quyên góp để bán lại')
        csdl.session.add_all([donate_type, exchange_type, donate_to_sell])
        try:
            csdl.session.commit()
            print("Đã thêm các loại DCType mặc định: 'quyên góp', 'trao đổi', 'quyên góp để bán lại'")
        except Exception as e:
            csdl.session.rollback()
            print(f"Lỗi khi thêm DCType: {e}")
    else:
        print("Bảng DCType đã có dữ liệu, bỏ qua khởi tạo.")
