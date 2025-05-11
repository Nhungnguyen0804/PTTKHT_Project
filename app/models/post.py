from app.flask_extensions import csdl

class Post(csdl.Model):
    __tablename__ = 'post'

    post_id = csdl.Column(csdl.String(50), primary_key=True)  # Khóa chính, kiểu chuỗi
    content = csdl.Column(csdl.String(500), nullable=False)   # Nội dung bài đăng
    image_url = csdl.Column(csdl.String(255), nullable=True)   # Link hình ảnh bài đăng
    is_approved = csdl.Column(csdl.Boolean, default=False)    # Cờ kiểm duyệt bài đăng
    status = csdl.Column(csdl.String(50), default='Not done')  # Trạng thái bài đăng (done, not done)
    post_type = csdl.Column(csdl.String(50), nullable=False)  # Loại bài đăng (thanh lý, trao đổi, donate)

    # Liên kết với User
    user_id = csdl.Column(csdl.Integer, csdl.ForeignKey('user.id'), nullable=False)

    # Liên kết với CategoryCategory
    category_id = csdl.Column(csdl.Integer, csdl.ForeignKey('category.id'), nullable=False)

    # Dùng post.user để truy cập user
    user = csdl.relationship('User', backref='posts')

    def __repr__(self):
        return f"<Post {self.post_id}>"
