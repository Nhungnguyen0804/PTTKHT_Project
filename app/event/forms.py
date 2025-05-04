from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField
from wtforms.validators import DataRequired

class MoneyDonationForm(FlaskForm):
    quantity = IntegerField('Giá trị', validators=[DataRequired()])

class ItemDonationForm(FlaskForm):
    itemName = StringField('Tên hiện vật', validators=[DataRequired()])
    quantity = IntegerField('Số lượng', validators=[DataRequired()])
    itemCategoryId = SelectField('Loại sản phẩm', coerce=int, validators=[DataRequired()])
