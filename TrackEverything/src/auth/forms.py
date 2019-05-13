from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from src.models import POSITION_CHOICES
from src.models.user import User


# Create user form
# TODO: See core/tasks/forms.py
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(2, 255, 'Incorrect length')])
    username = StringField('Username', validators=[DataRequired(), Length(2, 255, 'Incorrect length')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(2, 255, 'Incorrect length')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(2, 255, 'Incorrect length')])
    patronymic = StringField('Patronymic', Length(2, 255, 'Incorrect length'))
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
