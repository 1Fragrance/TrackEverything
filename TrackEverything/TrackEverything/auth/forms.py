from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import User, POSITION_CHOICES


# Create user form
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    patronymic = StringField('Patronymic')
    position = SelectField('Position', choices=POSITION_CHOICES, coerce=int, validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.objects(email=field.data):
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.objects(username=field.data):
            raise ValidationError('Username is already in use.')


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')