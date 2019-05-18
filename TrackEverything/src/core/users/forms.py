from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from src.models import POSITION_CHOICES
from src.models.user import User


# TODO: Do this shit
class UserAssignForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 255, 'Incorrect length')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(2, 255, 'Incorrect length')])
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
