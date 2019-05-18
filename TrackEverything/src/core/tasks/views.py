from . import task
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from .forms import TaskForm
from src.models.task import Task
from src.models.project import Project
from src.models.user import User
from ..views import is_admin
from bson import ObjectId


# Get all tasks
@task.route('/tasks', methods=['GET'])
@login_required
def list_tasks():
    task_list = Task.objects().all().select_related()
    return render_template('core/tasks/tasks.html',
                           tasks=task_list, title="Tasks")


@task.route('/tasks/<string:id>', methods=['GET'])
@login_required
def get_task(id):
    task = Task.objects(pk=id).first().select_related()
    return render_template('core/tasks/task_info.html',
                           task=task, title=task.name)


@task.route('/tasks/me', methods=['GET'])
@login_required
def users_tasks():
    tasks = Task.objects(performer=current_user.pk).select_related()
    return render_template('core/tasks/tasks.html', tasks=tasks, title="My tasks")


def fill_projects_and_users(form, id=None):
    project_names = Project.objects().values_list('pk', 'name')
    if not project_names:
        selected_project_performers = ()
    else:
        if id is None:
            id = project_names[0][0]
        selected_project_performers = User.objects(project=id).values_list('pk', 'username')

    for project in project_names:
        form.project.choices.append((str(project[0]), project[1]))

    for performer in selected_project_performers:
        form.performer.choices.append((str(performer[0]), performer[1]))


# Admin: create new task
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

            try:
                task.save()
                flash('You have successfully added a new task.')
            except Exception as e:
                flash('Error: task already exists.')

            return redirect(url_for('task.list_tasks'))

        return render_template('core/tasks/task.html', action="Add", add_task=add_task,
                               form=form, title="Add Task")


# admin edit task
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
        fill_projects_and_users(form, task.project.pk if task.project else None)

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
            try:
                task.save()
            except Exception as e:
                flash(str(e) + 'Error: task already exists.')

            flash('You have successfully edited the task.')

            return redirect(url_for('task.list_tasks'))

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


# Admin: delete task
@task.route('/tasks/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    if not is_admin():
        abort(403)
    else:
        # TODO: 404 error validation
        task = Task.objects(pk=id).first()
        task.delete()
        flash('You have successfully deleted the task.')

        return redirect(url_for('task.list_tasks'))

    # TODO add change status
