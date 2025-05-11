from app.flask_extensions import csdl

class Post(csdl.Model):
    __tablename__ = 'post'

    post_id = csdl.Column(csdl.String(50), primary_key=True)  # Khóa chính, kiểu chuỗi
    content = csdl.Column(csdl.String(500), nullable=False)   # Nội dung bài đăng
    image_url = csdl.Column(csdl.String(255), nullable=True)   # Link hình ảnh bài đăng
    is_approved = csdl.Column(csdl.Boolean, default=False)    # Cờ kiểm duyệt bài đăng , aaproved/ reject
    status = csdl.Column(csdl.String(50), default='pending')  # Trạng thái bài đăng pending/received item
    post_type = csdl.Column(csdl.String(50), nullable=False)  # Loại bài đăng (thanh lý, trao đổi, donate)
    create_date = csdl.Column(csdl.DateTime, default=csdl.func.now())  # Thời gian tạo bài đăng
    approval_date = csdl.Column(csdl.DateTime, nullable=True) # time duyệt
    submit_date = csdl.Column(csdl.DateTime, nullable=True)  # Thời gian kết thúc bài đăng
    # Liên kết với User
    user_id = csdl.Column(csdl.Integer, csdl.ForeignKey('user.id'), nullable=False)
    category_id = csdl.Column(csdl.Integer, csdl.ForeignKey('category.id'), nullable=False)
    
    interest_count = csdl.Column(csdl.Integer, default=0)
    interested_user_id = csdl.Column(csdl.Text, default='')
    # Dùng post.user để truy cập user
    user = csdl.relationship('User', backref='posts')

    def __repr__(self):
        return f"<Post {self.post_id}>"
