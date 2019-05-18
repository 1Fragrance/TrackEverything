from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, Regexp
from src.models import POSITION_CHOICES
from src.models.user import User
from ..tasks.forms import NonValidatingSelectField
from bson import ObjectId


class UserAssignForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 255, 'Incorrect length')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(2, 255, 'Incorrect length')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(2, 255, 'Incorrect length'),
                                                       Regexp("^[a-zA-Z-_]+$", message='Only latin letters')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(2, 255, 'Incorrect length'),
                                                     Regexp("^[a-zA-Z-_]+$", message='Only latin letters')])
    patronymic = StringField('Patronymic', validators=[Length(2, 255, 'Incorrect length'),
                                                       Regexp("^[a-zA-Z-_]+$", message='Only latin letters')])
    position = SelectField('Position', choices=POSITION_CHOICES, coerce=int, validators=[DataRequired()])
    tasks = SelectMultipleField('Tasks', choices=[], coerce=ObjectId, validators=[Optional()])
    project = NonValidatingSelectField('Project', choices=[])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if self.email.data != field.data and User.objects(email=field.data):
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if self.username.data != field.data and User.objects(username=field.data):
            raise ValidationError('Username is already in use.')
