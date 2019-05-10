from . import api
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from .forms import TaskForm, ProjectForm, UserAssignForm
from ..models import Task, Project, User


def is_admin():
    if not current_user.is_admin:
        return False
    return True

@api.route('/')
@login_required
def index():
    return render_template('api/index.html', title="Index page")


# Common part
# Task API
@api.route('/tasks', methods=['GET', 'POST'])
@login_required
def list_tasks():
    if is_admin():
        tasks = Task.objects.all()
    else:
        tasks = Task.objects(performers=current_user.pk)

    return render_template('api/tasks/tasks.html',
                           tasks=tasks, title="Tasks")

@api.route('/projects')
@login_required
def list_projects():
    if is_admin():
        projects = Project.objects.all()
    else:
        projects = Project.objects(participants=current_user.pk)
    return render_template('api/projects/projects.html',
                           projects=projects, title='Projects')


# Admin part
@api.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if not is_admin():
        abort(403)
    else:
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

            return redirect(url_for('api.list_tasks'))

        return render_template('api/tasks/task.html', action="Add", add_task=add_task,
                           form=form, title="Add Task")


# TODO add change status
@api.route('/tasks/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    if not is_admin():
        abort(403)
    else:
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

            return redirect(url_for('api.list_tasks'))

        form.name.data = task.name
        form.description.data = task.description
        form.status.data = task.status
        # form.start_date = task.start_date
        # form.end_date = form.end_date

        return render_template('api/tasks/task.html', action="Edit",
                            add_task=add_task, form=form,
                            task=task, title="Edit Task")


@api.route('/tasks/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    if not is_admin():
        abort(403)
    else:
        # TODO: 404 error validation
        task = Task.objects(pk=id).first()
        task.delete()
        flash('You have successfully deleted the task.')

        return redirect(url_for('api.list_tasks'))
        return render_template(title="Delete Task")


# Project API



@api.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if not is_admin():
        abort(403)
    else:
        add_project = True
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project(name=form.name.data,
                              short_name=form.short_name.data,
                              description=form.description.data,
                              status=form.status.data)
            try:
                project.save()
                flash('You have successfully added a new project.')
            except:
                flash('Error: project already exists.')

            return redirect(url_for('api.list_projects'))


        return render_template('api/projects/project.html', add_project=add_project,
                                form=form, title='Add Project')


@api.route('/projects/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    if not is_admin():
        abort(403)
    else:
        add_project = False
        project = Project.objects(pk=id).first()
        form = ProjectForm(obj=project)

        if form.validate_on_submit():
            project.name = form.name.data
            project.short_name = form.short_name.data
            project.description = form.description.data
            project.status = form.status.data

            project.save()
            flash('You have successfully edited the project.')

            return redirect(url_for('api.list_projects'))

        form.name.data = project.name
        form.short_name.data = project.short_name
        form.description.data = project.description
        form.status.data = project.status

        return render_template('api/projects/project.html', add_project=add_project,
                                form=form, title="Edit Project")


@api.route('/projects/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    if not is_admin():
        abort(403)
    else:
        project = Project.objects(pk=id).first()
        project.delete()
        flash('You have successfully deleted the project.')

        return redirect(url_for('api.list_projects'))
        return render_template(title="Delete Project")


# User API
@api.route('/users')
@login_required
def list_users():
    if not is_admin():
        abort(403)
    else:
        users = User.objects.all()
        return render_template('api/users/users.html',
                                users=users, title='Users')


@api.route('/users/assign/<string:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    if not is_admin():
        abort(403)
    else:
        user = User.objects(pk=id).first()

        # TODO: Think about this opportunity
        if user.is_admin:
            abort(403)

        form = UserAssignForm(obj=user)
        if form.validate_on_submit():
            user.project = form.department.data
            user.task = form.role.data
            user.save()
            flash('You have successfully assigned a project and tasks.')

            return redirect(url_for('api.list_users'))

        return render_template('api/users/user.html',
                                user=user, form=form,
                                title='Assign User')
