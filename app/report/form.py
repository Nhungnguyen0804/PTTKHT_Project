from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
# FlaskForm để chọn năm
class YearForm(FlaskForm):

    year = SelectField('Chọn năm',
                       coerce=int, # Dữ liệu của field này sẽ là int nếu hợp lệ
                       validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        current_year = datetime.now().year
        # Tạo danh sách các năm từ 2020 đến năm hiện tại
        self.year.choices = [(y, str(y)) for y in range(2020, current_year + 1)]

