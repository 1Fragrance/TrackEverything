from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from src.common.messages import (EMAIL_EXIST_MESSAGE, INCORRECT_LENGTH_MESSAGE,
                                 ONLY_LETTERS_MESSAGE, USERNAME_EXIST_MESSAGE)
from src.common.validation import (MAX_STRING_LENGTH, MIN_STRING_LENGTH,
                                   REGEX_LATIN_LETTERS)
from src.models import POSITION_CHOICES
from src.models.user import User

"""
Create user form
 
"""
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(
        MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE)])
    username = StringField('Username', validators=[DataRequired(), Length(
        MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                     Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    patronymic = StringField('Patronymic', validators=[Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    position = SelectField('Position', choices=POSITION_CHOICES,
                           coerce=int, validators=[DataRequired()])

    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.objects(email=field.data):
            raise ValidationError(EMAIL_EXIST_MESSAGE)

    def validate_username(self, field):
        if User.objects(username=field.data):
            raise ValidationError(USERNAME_EXIST_MESSAGE)


"""
Login form

"""
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
