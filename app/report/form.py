from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
# FlaskForm để chọn năm
class YearForm(FlaskForm):
    year = SelectField('Chọn năm',
                       coerce=int, # Dữ liệu của field này sẽ là int nếu hợp lệ
                       validators=[DataRequired(message="Vui lòng chọn một năm.")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        current_year = datetime.now().year
        # Choices: (value, label). Value là int do coerce=int.
        self.year.choices = [(y, str(y)) for y in range(2020, current_year + 1)]