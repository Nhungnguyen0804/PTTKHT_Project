from flask_wtf import FlaskForm
from wtforms import  PasswordField, SubmitField, StringField, DateField, SelectField, EmailField
from wtforms.validators import DataRequired,  EqualTo

class changePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')


class editProfileForm(FlaskForm):
    hoTen = StringField('Họ và tên')
    ngaySinh = DateField('Ngày sinh')
    gioiTinh = SelectField('Giới tính', choices=[
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('other', 'Khác')])
    
    address = StringField('Địa chỉ')
    email = EmailField('Email')
    phone = StringField('Số diện thoại')
    fb = StringField('Facebook')
    zalo = StringField('Zalo')
    submit = SubmitField('Save')