from app.flask_extensions import csdl

class Post(csdl.Model):
    __tablename__ = 'post'

    post_id = csdl.Column(csdl.String(50), primary_key=True)  # Khóa chính, kiểu chuỗi
    content = csdl.Column(csdl.String(500), nullable=False)   # Nội dung bài đăng
    image_url = csdl.Column(csdl.String(255), nullable=True)   # Link hình ảnh bài đăng
    is_approved = csdl.Column(csdl.Boolean, default=False)    # Cờ kiểm duyệt bài đăng

    def __repr__(self):
        return f"<Post {self.post_id}>"
