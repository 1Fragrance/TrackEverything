from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from src.models import STATUS_CHOICES


# Project view form
class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    short_name = StringField('Short name', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    # tasks
    submit = SubmitField('Submit')
