from . import task
from flask import abort, flash, redirect, render_template, url_for, jsonify
from flask_login import current_user, login_required
from .forms import TaskForm
from src.models.task import Task
from src.models.project import Project
from src.models.user import User
from ..views import is_admin


# Get all tasks
@task.route('/tasks', methods=['GET', 'POST'])
@login_required
def list_tasks():
    if is_admin():
        tasks = Task.objects.all()
    else:
        tasks = Task.objects(performers=current_user.pk)

    return render_template('core/tasks/tasks.html',
                           tasks=tasks, title="Tasks")


# Admin: create new task
@task.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if not is_admin():
        abort(403)
    else:
        add_task = True
        form = TaskForm()

        project_names = Project.objects().values_list('pk', 'name')
        if not project_names:
            selected_project_performers = ()
        else:
            selected_project_performers = User.objects(project=project_names[0][0]).values_list('pk', 'username')

        for project in project_names:
            form.project.choices.append((project[0], project[1]))

        for performer in selected_project_performers:
            form.performers.choices.append((performer[0], performer[1]))

        if form.validate_on_submit():
            task = Task(name=form.name.data,
                        description=form.description.data,
                        status=form.status.data,
                        start_date=form.start_date.data,
                        end_date=form.end_date.data,
                        project=form.project.data,
                        performers=form.performers.data or [])
            try:
                task.save()
                flash('You have successfully added a new task.')
            except Exception as e:
                flash('Error: task already exists.')

            return redirect(url_for('core.list_tasks'))

        return render_template('core/tasks/task.html', action="Add", add_task=add_task,
                               form=form, title="Add Task")


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

        return redirect(url_for('core.list_tasks'))
        return render_template(title="Delete Task")

    # TODO add change status


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

        if form.validate_on_submit():
            task.name = form.name.data
            task.description = form.description.data
            task.status = form.status.data
            # task.start_date = form.start_date
            # task.end_date = form.end_date
            task.save()
            flash('You have successfully edited the task.')

            return redirect(url_for('core.list_tasks'))

        form.name.data = task.name
        form.description.data = task.description
        form.status.data = task.status
        form.start_date.data = task.start_date
        form.end_date.data = task.end_date

        project_users = User.objects(project=task.project).values_list('pk', 'username')
        for user in project_users:
            form.performers.choices.append((user[0], user[1]))

        form.performers.data = task.performers

        return render_template('core/tasks/task.html', action="Edit",
                               add_task=add_task, form=form,
                               task=task, title="Edit Task")
