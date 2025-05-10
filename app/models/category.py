from flask_login import UserMixin
from app.flask_extensions import csdl, login_manager
from datetime import datetime

class Category(UserMixin, csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    category_name = csdl.Column(csdl.String(50), unique=True, nullable=False)
    

def init_categories():
    """Hàm khởi tạo """
    if Category.query.count() == 0:
        categories = [
            "Sách giáo khoa",
            "Sách tham khảo",
            "Vở, sổ tay",
            "Máy tính bỏ túi",
            "Dụng cụ học tập (bút, thước, compa)",
            
            "Tai nghe",
            "Bàn phím, chuột",
            "Máy tính cũ",
            "Sạc dự phòng, dây sạc",
            "Áo dài",
            "Đồng phục",
            "Trang phục thể thao",
            "Áo khoác đồng phục",
            "Giày",
            "Bóng đá/Bóng chuyền/Bóng rổ",
            "Vợt cầu lông/bóng bàn",
          
            "Đạo cụ sân khấu, Nhạc cụ",
            "Balo / túi xách",
            "Bình nước, hộp cơm",
            "Móc khóa / phụ kiện nhỏ",
            "Quà tặng không dùng đến",
            "Sổ lưu bút",
            "Thiệp, đồ lưu niệm"
        ]

        for name in categories:
            category = Category(category_name=name)
            csdl.session.add(category)

      
        csdl.session.commit()
        print("Đã thêm các loại đồ quyên góp")
        
    else:
        print("Bảng Category đã có dữ liệu, bỏ qua khởi tạo.")