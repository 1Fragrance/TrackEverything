from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, Regexp
from wtforms.fields.html5 import DateField
from src.models import STATUS_CHOICES
from src.common.validation import REGEX_LATIN_LETTERS, DATE_FORMAT, MAX_STRING_LENGTH, MIN_STRING_LENGTH
from src.common.messages import INCORRECT_LENGTH_MESSAGE, ONLY_LETTERS_MESSAGE, START_DATE_LESS_THAN_END_MESSAGE, START_DATE_LESS_THAN_TODAY_MESSAGE


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        """pre_validation is disabled"""
        pass


# Task view form
# TODO: Move messages to consts or resx
class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(MIN_STRING_LENGTH, MAX_STRING_LENGTH, INCORRECT_LENGTH_MESSAGE),
                                           Regexp(REGEX_LATIN_LETTERS, message=ONLY_LETTERS_MESSAGE)])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    start_date = DateField('Start date', format=DATE_FORMAT, validators=[DataRequired()])
    end_date = DateField('End date', format=DATE_FORMAT, validators=[Optional()])
    project = NonValidatingSelectField('Project', choices=[])
    performer = NonValidatingSelectField('Performer', choices=[])
    submit = SubmitField('Submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
    
        st_date = datetime.combine(self.start_date.data, datetime.min.time())
        
        if st_date < datetime.utcnow() - timedelta(days=1):
            self.start_date.errors.append(START_DATE_LESS_THAN_TODAY_MESSAGE)
            result = False
        if self.end_date.data:
            ed_date = datetime.combine(self.end_date.data, datetime.min.time())
            if ed_date < st_date:
                self.end_date.errors.append(START_DATE_LESS_THAN_END_MESSAGE)
                result = False
        
        return result
