from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, Length, Optional, Regexp,
                                ValidationError)

from src.common.messages import (EMAIL_EXIST_MESSAGE, INCORRECT_LENGTH_MESSAGE,
                                 ONLY_LETTERS_MESSAGE,
                                 ONLY_NUMBERS_AND_LETTERS_MESSAGE,
                                 USERNAME_EXIST_MESSAGE)
from src.common.validation import (MAX_STRING_LENGTH, MIN_STRING_LENGTH,
                                   REGEX_LATIN_LETTERS, REGEX_NUMBERS_LETTERS)
from src.models import POSITION_CHOICES
from src.models.user import User

from ..tasks.forms import NonValidatingSelectField


"""

User assign form
"""
class UserAssignForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(
        MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE), Regexp(REGEX_NUMBERS_LETTERS, message=ONLY_NUMBERS_AND_LETTERS_MESSAGE)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(
        MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                     Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    patronymic = StringField('Patronymic', validators=[Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    position = SelectField('Position', choices=POSITION_CHOICES,
                           coerce=int, validators=[DataRequired()])
    tasks = SelectMultipleField(
        'Tasks', choices=[], coerce=ObjectId, validators=[Optional()])
    project = NonValidatingSelectField('Project', choices=[])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if self.email.data != field.data and User.objects(email=field.data):
            raise ValidationError(EMAIL_EXIST_MESSAGE)

    def validate_username(self, field):
        if self.username.data != field.data and User.objects(username=field.data):
            raise ValidationError(USERNAME_EXIST_MESSAGE)
