from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,SelectMultipleField
from wtforms.validators import DataRequired, Optional
from ..models import STATUS_CHOICES, Project, Task
from wtforms.fields.html5 import DateField
from bson import ObjectId

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


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    short_name = StringField('Short name', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])
    status = SelectField('Status', choices=STATUS_CHOICES, coerce=int, validators=[DataRequired()])
    # tasks
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    task = SelectField('Task')
    project = SelectField('Project')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(UserAssignForm, self).__init__(*args, **kwargs)
        self.task.choices = [(a.id, a.name) for a in Task.objects.all()]
        self.project.choices = [(a.id, a.name) for a in Project.objects.all()]


