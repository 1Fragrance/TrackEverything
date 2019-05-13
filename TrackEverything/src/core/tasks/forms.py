from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, ValidationError
from wtforms.fields.html5 import DateField
from bson import ObjectId
from src.models import STATUS_CHOICES


# Task view form
# TODO: Think about max_length validation and enddate < startdate
# TODO: Think about more difficult logic for statuses
# TODO: Move messages to consts or resx
class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(5, 255, 'Incorrect length')])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    start_date = DateField('Start date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', validators=[Optional()])
    project = SelectField('Project', choices=[], coerce=ObjectId, validators=[Optional()])
    performer = SelectField('Performers', choices=[], coerce=ObjectId, validators=[Optional()])
    submit = SubmitField('Submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        st_date = self.start_date.data
        ed_date = self.end_date.data
        if st_date < datetime.today():
            raise ValidationError('Start date cannot be less than today')
        if ed_date and ed_date < st_date:
            raise ValidationError('Start date have to be less than end date')

        return True
