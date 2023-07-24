from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class Finan(FlaskForm):
    data = StringField(name='data')
    item = StringField('item')
    vendor = StringField('vendor')
    specification = StringField('specification')
    unit = StringField('unit')
    amount = StringField('amount')
    unit_price = StringField('unit_price')
    price = StringField('price')
    remark = StringField('remark')
    category = StringField('category')
    submit = SubmitField('submit')




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')




class Pay(FlaskForm):
    clientName = StringField(name='clientName')
    productName = StringField(name="productName")
    price = StringField(name='price')
    timeStart = StringField(name='timeStart')
    timeEnd = StringField(name= 'timeEnd')
    time = StringField(name = 'time')
    status = StringField(name='status')
    note = StringField(name='note')