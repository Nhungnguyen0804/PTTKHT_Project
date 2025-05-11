from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
# FlaskForm để chọn năm
class YearForm(FlaskForm):
    year = SelectField('Chọn năm', coerce=int, validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(YearForm, self).__init__(*args, **kwargs)
        current_year = datetime.now().year
        # Tạo danh sách các năm từ 2010 đến năm hiện tại
        self.year.choices = [(year, str(year)) for year in range(2010, current_year + 1)]
        self.year.default = current_year  # Mặc định là năm hiện tại