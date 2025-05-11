from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from datetime import datetime

class FilterForm(FlaskForm):
    sort_order = SelectField(
        'Sắp xếp theo',
        choices=[
            ('desc', 'Mới nhất'),
            ('asc', 'Cũ nhất')
        ],
        validators=[DataRequired()]
    )
    post_type = SelectField(
        'Loại bài đăng',
        choices=[
            ('all', 'Tất cả'),
            ('Thanh Lý', 'Thanh Lý'),
            ('Trao Đổi', 'Trao Đổi'),
            ('Donate', 'Đóng Góp')
        ],
        validators=[DataRequired()]
    )