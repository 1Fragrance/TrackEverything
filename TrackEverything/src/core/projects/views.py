from . import project
from flask import abort, flash, redirect, render_template, url_for, jsonify
from flask_login import current_user, login_required
from .forms import ProjectForm
from src.models.task import Task
from src.models.project import Project
from src.models.user import User
from ..views import is_admin


# Get all projects
@project.route('/projects')
@login_required
def list_projects():
    if is_admin():
        projects = Project.objects.all()
    else:
        projects = Project.objects(participants=current_user.pk)
    return render_template('core/projects/projects.html',
                           projects=projects, title='Projects')


# Admin: add new project
@project.route('/projects/add', methods=['GET', 'POST'])
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
            # TODO: PRG Pattern
            return redirect(url_for('core.list_projects'))

        return render_template('core/projects/project.html', add_project=add_project,
                               form=form, title='Add Project')


# Admin: Edit project
@project.route('/projects/edit/<string:id>', methods=['GET', 'POST'])
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

            return redirect(url_for('core.list_projects'))

        form.name.data = project.name
        form.short_name.data = project.short_name
        form.description.data = project.description
        form.status.data = project.status

        return render_template('core/projects/project.html', add_project=add_project,
                               form=form, title="Edit Project")


# Admin: delete project
@project.route('/projects/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    if not is_admin():
        abort(403)
    else:
        project = Project.objects(pk=id).first()
        project.delete()
        flash('You have successfully deleted the project.')

        return redirect(url_for('core.list_projects'))
        return render_template(title="Delete Project")


# API Part
# Get project tasks
@project.route('/projects/<project_id>/tasks')
def get_project_tasks(project_id):
    tasks = Task.objects(project=project_id).values_list('pk', 'name')

    tasks_array = []

    for task in tasks:
        task_obj = {'pk': str(task[0]), 'name': task[1]}
        tasks_array.append(task_obj)

    return jsonify({'tasks': tasks_array})


# Get project participants
@project.route('/projects/<project_id>/users')
def get_project_users(project_id):
    users = User.objects(project=project_id).values_list('pk', 'username')

    users_array = []

    for user in users:
        user_obj = {'pk': str(user[0]), 'username': user[1]}
        users_array.append(user_obj)

    return jsonify({'users': users_array})
