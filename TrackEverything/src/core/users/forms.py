from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


# User edit form
class UserAssignForm(FlaskForm):
    task = SelectField('Task')
    project = SelectField('Project')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(UserAssignForm, self).__init__(*args, **kwargs)
        self.task.choices = [(a.id, a.name) for a in Task.objects.all()]
        self.project.choices = [(a.id, a.name) for a in Project.objects.all()]
