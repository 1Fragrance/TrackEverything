from datetime import datetime

from bson import ObjectId
from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.common.messages import (TASK_ADDED_MESSAGE, TASK_DELETED_MESSAGE,
                                 TASK_EDITED_MESSAGE, TASK_UPDATED_MESSAGE)
from src.models import STATUS_CHOICES
from src.models.project import Project
from src.models.task import Task
from src.models.user import User

from ..views import is_admin
from . import task
from .forms import TaskForm


"""
Get all tasks endpoint

"""
@task.route('/tasks', methods=['GET'])
@login_required
def list_tasks():
    task_list = Task.objects().all().select_related()
    return render_template('core/tasks/tasks.html',
                           tasks=task_list, statuses=STATUS_CHOICES, title="Tasks")


"""
Get task endpoint

"""
@task.route('/tasks/<string:id>', methods=['GET'])
@login_required
def get_task(id):
    task = Task.objects(pk=id).first().select_related()
    if not task:
        abort(404)

    return render_template('core/tasks/task_info.html',
                           task=task, statuses=STATUS_CHOICES, title=task.name)


"""

Update task endpoint
"""
@task.route('/tasks/<string:id>/update/<int:status>', methods=['GET'])
@login_required
def update_task_status(id, status):
    task = Task.objects(pk=id).first()
    if not task:
        abort(404)

    if not is_admin() and task.performer == current_user.pk:
        abort(403)
        if status <= len(STATUS_CHOICES):
            raise Exception
        task.status = status
        task.save()
        flash(TASK_UPDATED_MESSAGE)

    return render_template('core/tasks/task_info.html',
                           task=task, statuses=STATUS_CHOICES, title=task.name)


"""

Own task endpoint
"""
@task.route('/tasks/me', methods=['GET'])
@login_required
def users_tasks():
    tasks = Task.objects(performer=current_user.pk).select_related()
    return render_template('core/tasks/tasks.html', statuses=STATUS_CHOICES, tasks=tasks, title="My tasks")

"""

Fill form project and performers
"""
def fill_projects_and_users(form, id=None):
    project_names = Project.objects().values_list('pk', 'name')
    if not project_names:
        selected_project_performers = ()
    else:
        if id is None:
            id = project_names[0][0]
        selected_project_performers = User.objects(
            project=id).values_list('pk', 'username')

    for project in project_names:
        form.project.choices.append((str(project[0]), project[1]))

    for performer in selected_project_performers:
        form.performer.choices.append((str(performer[0]), performer[1]))


"""

Admin: create new task endpoint
"""
@task.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if not is_admin():
        abort(403)
    else:
        add_task = True
        form = TaskForm()
        fill_projects_and_users(form)

        if request.method == 'POST' and form.validate_on_submit():
            task = Task(name=form.name.data,
                        description=form.description.data,
                        status=form.status.data,
                        start_date=form.start_date.data,
                        end_date=form.end_date.data)
            if form.performer.raw_data:
                task.performer = ObjectId(form.performer.data)
            if form.project.raw_data:
                task.project = ObjectId(form.project.data)

            task.save()
            flash(TASK_ADDED_MESSAGE)
            return redirect(url_for('task.get_task', id=task.pk))

        return render_template('core/tasks/task.html', action="Add", add_task=add_task,
                               form=form, title="Add Task")


"""

Admin: edit task endpoint
"""
@task.route('/tasks/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    if not is_admin():
        abort(403)
    else:
        task = Task.objects(pk=id).first()
        if not task:
            abort(404)

        add_task = False
        form = TaskForm(obj=task)
        fill_projects_and_users(
            form, task.project.pk if task.project else None)

        if request.method == 'POST' and form.validate_on_submit():
            task.name = form.name.data
            task.description = form.description.data
            task.status = form.status.data
            task.start_date = form.start_date.data
            task.end_date = form.end_date.data
            task.update_date = datetime.utcnow
            if form.performer.raw_data:
                task.performer = ObjectId(form.performer.data)
            else:
                task.performer = None
            if form.project.raw_data:
                task.project = ObjectId(form.project.data)
            else:
                task.project = None

            task.save()    

            flash(TASK_EDITED_MESSAGE)
            return redirect(url_for('task.get_task', id=task.pk))

        form.name.data = task.name
        form.description.data = task.description
        form.status.data = task.status
        form.start_date.data = task.start_date
        if task.end_date:
            form.end_date.data = task.end_date

        if task.project:
            form.project.data = str(task.project.pk)
        if task.performer:
            form.performer.data = str(task.performer.pk)

        return render_template('core/tasks/task.html', action="Edit",
                               add_task=add_task, form=form,
                               task=task, title="Edit Task")


"""

Admin: delete task endpoint
"""
@task.route('/tasks/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    if not is_admin():
        abort(403)
    else:
        task = Task.objects(pk=id).first()
        if not task:
            abort(404)

        task.delete()
        flash(TASK_DELETED_MESSAGE)

        return redirect(url_for('task.list_tasks'))
