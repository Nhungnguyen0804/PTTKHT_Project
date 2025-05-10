from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired
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
        ('quyen_gop', 'Quyên góp'),
        ('quyen_gop_trao_doi', 'Quyên góp và trao đổi')
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

    endDate = DateTimeField('Thời gian kết thúc', 
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )