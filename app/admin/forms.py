from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileField

class EventAdderForm(FlaskForm):
    name = StringField('Tên sự kiện', validators=[DataRequired()])
    
    startTime = DateTimeField('Thời gian bắt đầu', 
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )

    endTime = DateTimeField('Thời gian kết thúc', 
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )

    eventType = SelectField('Loại sự kiện', choices=[
        ('Quyên góp', 'Quyên góp'),
        ('Quyên góp và trao đổi', 'Quyên góp và trao đổi')
    ], validators=[DataRequired()])
    image = FileField('Ảnh sự kiện', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Chỉ chấp nhận ảnh!')
    ])
    submit = SubmitField('Thêm sự kiện')
    
class DonationCategoryAdderForm(FlaskForm):
    name = StringField('Tên hạng mục quyên góp', validators=[DataRequired()])
    donationType = SelectField('Loại hình quyên góp', choices=[
        ('money', 'Tiền'),
        ('item', 'Hiện vật')
    ], validators=[DataRequired()])
    targetQuantity = IntegerField('Mục tiêu', validators=[DataRequired()])
    submit = SubmitField('Thêm sự kiện')
    startDate = DateTimeField('Thời gian bắt đầu', 
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )
    dcType = SelectField('Loại hạng mục', choices=[
        (1, 'Quyên góp'),
        (2, 'Trao đổi'),
        (3, 'Quyên góp để bán lại')
    ])
    endDate = DateTimeField('Thời gian kết thúc', 
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )

class BuyableItemForm(FlaskForm):
    item_name = StringField('Tên vật phẩm', validators=[DataRequired()])
    price = IntegerField('Giá (VNĐ)', validators=[NumberRange(min=0)])
    image = FileField('Ảnh vật phẩm', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'])])
    submit = SubmitField('Lưu')