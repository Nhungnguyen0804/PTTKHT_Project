from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileField

class MoneyDonationForm(FlaskForm):
    quantity = IntegerField('Giá trị', validators=[DataRequired()])

class ItemDonationForm(FlaskForm):
    itemName = StringField('Tên hiện vật', validators=[DataRequired()])
    quantity = IntegerField('Số lượng', validators=[DataRequired()])
    itemCategoryId = SelectField('Loại sản phẩm', coerce=int, validators=[DataRequired()])
    image = image = FileField('Ảnh hiện vật', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Chỉ chấp nhận ảnh!')
    ])
