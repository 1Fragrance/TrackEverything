from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from datetime import datetime, date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, ValidationError, Email
from wtforms.fields.html5 import DateField
from bson import ObjectId
from src.models import STATUS_CHOICES, POSITION_CHOICES
from src.models.user import User
from src.models.task import Task
from src.models.project import Project

# TODO: Do this shit
class UserAssignForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 255, 'Incorrect length')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(2, 255, 'Incorrect length')])
    username = StringField('Username', validators=[DataRequired(), Length(2, 255, 'Incorrect length')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(2, 255, 'Incorrect length')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(2, 255, 'Incorrect length')])
    patronymic = StringField('Patronymic', validators=[Length(2, 255, 'Incorrect length')])
    position = SelectField('Position', choices=POSITION_CHOICES, coerce=int, validators=[DataRequired()])
    tasks = SelectField('Task')
    project = SelectField('Project')

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.objects(email=field.data):
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.objects(username=field.data):
            raise ValidationError('Username is already in use.')
