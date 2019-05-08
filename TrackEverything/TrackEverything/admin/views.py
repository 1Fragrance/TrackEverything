from . import admin
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from .forms import TaskForm
from ..models import Task


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/admin/dashboard')
@login_required
def dashboard():
    check_admin()
    return render_template('admin/dashboard.html', title="Dashboard")


@admin.route('/tasks', methods=['GET', 'POST'])
@login_required
def list_tasks():
    check_admin()
    tasks = Task.objects.all()

    return render_template('admin/tasks/tasks.html',
                           tasks=tasks, title="Tasks")


@admin.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    check_admin()

    add_task = True
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,
                    description=form.description.data,
                    status=form.status.data)
                    # start_date=form.start_date.data,
                    # end_date=form.end_date.data)
        try:
            task.save()
            flash('You have successfully added a new task.')
        except:
            flash('Error: task already exists.')

        return redirect(url_for('admin.list_tasks'))

    return render_template('admin/tasks/task.html', action="Add", add_task=add_task,
                           form=form, title="Add Task")


@admin.route('/tasks/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    check_admin()

    add_task = False
    task = Task.objects(pk=id).first()
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        task.status = form.status.data
        # task.start_date = form.start_date
        # task.end_date = form.end_date
        task.save()
        flash('You have successfully edited the task.')

        return redirect(url_for('admin.list_tasks'))

    form.name.data = task.name
    form.description.data = task.description
    form.status.data = task.status
    # form.start_date = task.start_date
    # form.end_date = form.end_date

    return render_template('admin/tasks/task.html', action="Edit",
                           add_task=add_task, form=form,
                           task=task, title="Edit Task")


@admin.route('/tasks/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    check_admin()
    # TODO: 404 error validation
    task = Task.objects(pk=id).first()
    task.delete()
    flash('You have successfully deleted the task.')
    flash('You have successfully deleted the task.')

    return redirect(url_for('admin.list_tasks'))

    return render_template(title="Delete Task")