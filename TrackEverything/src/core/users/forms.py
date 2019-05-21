from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, Regexp
from src.models import POSITION_CHOICES
from src.models.user import User
from ..tasks.forms import NonValidatingSelectField
from bson import ObjectId
from src.common.validation import REGEX_LATIN_LETTERS, MAX_STRING_LENGTH, MIN_STRING_LENGTH
from src.common.messages import INCORRECT_LENGTH_MESSAGE, ONLY_LETTERS_MESSAGE, EMAIL_EXIST_MESSAGE, USERNAME_EXIST_MESSAGE


class UserAssignForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                     Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    patronymic = StringField('Patronymic', validators=[Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    position = SelectField('Position', choices=POSITION_CHOICES, coerce=int, validators=[DataRequired()])
    tasks = SelectMultipleField('Tasks', choices=[], coerce=ObjectId, validators=[Optional()])
    project = NonValidatingSelectField('Project', choices=[])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if self.email.data != field.data and User.objects(email=field.data):
            raise ValidationError(EMAIL_EXIST_MESSAGE)

    def validate_username(self, field):
        if self.username.data != field.data and User.objects(username=field.data):
            raise ValidationError(USERNAME_EXIST_MESSAGE)
