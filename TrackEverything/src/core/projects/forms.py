from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, ValidationError, Regexp
from bson import ObjectId
from src.models import STATUS_CHOICES
from src.models.project import Project


# Project view form
# TODO: See tasks/forms.py
class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(3, 255, 'Incorrect length'),
                                           Regexp("^[a-zA-Z-_]+$", message='Only latin letters')])
    short_name = StringField('Short name', validators=[DataRequired(), Length(3, 255, 'Incorrect length'),
                                                       Regexp("^[a-zA-Z-_]+$", message='Only latin letters')])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    participants = SelectMultipleField('Participants', choices=[], coerce=ObjectId, validators=[Optional()])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if self.name.data != field.data and Project.objects(name=field.data):
            # app.logger.info('ValidationError: Project name is already in use.')
            raise ValidationError('Project name is already in use.')

    def validate_short_name(self, field):
        if self.short_name.data != field.data and Project.objects(short_name=field.data):
            # app.logger.info('ValidationError: Short name is already in use.')
            raise ValidationError('Short name is already in use.')
