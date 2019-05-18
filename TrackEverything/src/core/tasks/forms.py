from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, Regexp
from wtforms.fields.html5 import DateField
from src.models import STATUS_CHOICES


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        """pre_validation is disabled"""
        pass


# Task view form
# TODO: Move messages to consts or resx
class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(3, 255, 'Incorrect length'),
                                           Regexp("^[a-zA-Z-_]+$", message='Only latin letters')])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    start_date = DateField('Start date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', validators=[Optional()])
    project = NonValidatingSelectField('Project', choices=[])
    performer = NonValidatingSelectField('Performer', choices=[])
    submit = SubmitField('Submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
    
        st_date = datetime.combine(self.start_date.data, datetime.min.time())
        
        if st_date < datetime.utcnow() - timedelta(days=1):
            self.start_date.errors.append('Start date cannot be less than today')
            result = False
        if self.end_date.data:
            ed_date = datetime.combine(self.end_date.data, datetime.min.time())
            if ed_date < st_date:
                self.end_date.errors.append('Start date have to be less than end date')
                result = False
        
        return result
