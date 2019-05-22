from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import (SelectField, SelectMultipleField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from src.common.messages import (INCORRECT_LENGTH_MESSAGE,
                                 ONLY_LETTERS_MESSAGE,
                                 ONLY_NUMBERS_AND_LETTERS_MESSAGE,
                                 PROJECT_NAME_EXIST_MESSAGE,
                                 SHORT_NAME_EXIST_MESSAGE)
from src.common.validation import (MAX_STRING_LENGTH, MIN_STRING_LENGTH,
                                   REGEX_LATIN_LETTERS, REGEX_NUMBERS_LETTERS)
from src.models import STATUS_CHOICES
from src.models.project import Project


# Project view form
# TODO: See tasks/forms.py
class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                           Regexp(REGEX_NUMBERS_LETTERS, message=ONLY_NUMBERS_AND_LETTERS_MESSAGE)])
    short_name = StringField('Short name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                                       Regexp(REGEX_NUMBERS_LETTERS, message=ONLY_NUMBERS_AND_LETTERS_MESSAGE)])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES,
                         coerce=int, validators=[DataRequired()])
    participants = SelectMultipleField(
        'Participants', choices=[], coerce=ObjectId, validators=[Optional()])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if self.name.data != field.data or Project.objects(name=field.data):
            raise ValidationError(PROJECT_NAME_EXIST_MESSAGE)

    def validate_short_name(self, field):
        if self.short_name.data != field.data or Project.objects(short_name=field.data):
            raise ValidationError(SHORT_NAME_EXIST_MESSAGE)
