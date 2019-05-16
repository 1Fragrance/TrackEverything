from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length
from bson import ObjectId
from src.models import STATUS_CHOICES


# Project view form
# TODO: See tasks/forms.py
class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(3, 255, 'Incorrect length')])
    short_name = StringField('Short name', validators=[DataRequired(), Length(3, 255, 'Incorrect length')])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    participants = SelectMultipleField('Participants', choices=[], coerce=ObjectId, validators=[Optional()])
    submit = SubmitField('Submit')

