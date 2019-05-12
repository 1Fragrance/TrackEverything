from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import DateField
from bson import ObjectId
from src.models import STATUS_CHOICES


# Task view form
# TODO: Think about max_length validation and enddate < startdate
# TODO: Think about more difficult logic for statuses
class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    start_date = DateField('Start date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', validators=[Optional()])
    project = SelectField('Project', choices=[], coerce=ObjectId, validators=[DataRequired()])
    performers = SelectMultipleField('Performers', choices=[], coerce=ObjectId, validators=[Optional()], default=[])
    submit = SubmitField('Submit')
