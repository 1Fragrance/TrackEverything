from datetime import datetime
from . import project
from flask import abort, flash, redirect, render_template, url_for, jsonify, request
from flask_login import current_user, login_required
from .forms import ProjectForm
from src.models.task import Task
from src.models.project import Project
from src.models.user import User
from ..views import is_admin
from mongoengine import Q
from bson import ObjectId


# Get all projects
@project.route('/projects')
@login_required
def list_projects():
    projects = Project.objects.all()

    return render_template('core/projects/projects.html',
                           projects=projects, title='Projects')


# Get users without project from DB
def fill_free_users(form):
    users_names = User.objects(Q(project__exists=False)).values_list('pk', 'username')
    for user in users_names:
        form.participants.choices.append((user[0], user[1]))


def fill_free_and_relative_users(form, project_id):
    users_names = User.objects(Q(project=project_id) | Q(project__exists=False)).values_list('pk', 'username')
    for user in users_names:
        form.participants.choices.append((user[0], user[1]))
    

# Admin: add new project
@project.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if not is_admin():
        abort(403)
    else:
        add_project = True
        form = ProjectForm()
        fill_free_users(form)
        if request.method == 'POST' and form.validate_on_submit():
            new_project = Project(name=form.name.data,
                                  short_name=form.short_name.data,
                                  description=form.description.data,
                                  status=form.status.data)
            try:
                new_project.save()

                for user_pk in form.participants.data:
                    User.objects(pk=user_pk).update_one(set__project=new_project.pk)
                flash('You have successfully added a new project.')
            # TODO: Remove this shitty warning
            except:
                # TODO: make normal messages
                flash('Error: project already exists.')
            # TODO: PRG Pattern
            return redirect(url_for('project.list_projects'))

       

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
        fill_free_and_relative_users(form, project.pk)
        
        if request.method == 'POST' and form.validate_on_submit():
            try:
                project.name = form.name.data
                project.short_name = form.short_name.data
                project.description = form.description.data
                project.status = form.status.data
                project.update_date = datetime.utcnow()
                project.save()
                
                for old_user in User.objects(project=project.pk):
                    old_user.update(unset__project=1)
                
                User.objects(pk__in=form.participants.raw_data).update(project=project.pk)

                flash('You have successfully edited the project.')
            except Exception as e:
                flash(str(e) + 'smth goes wrong')

            return redirect(url_for('project.list_projects'))
        
        form.name.data = project.name
        form.short_name.data = project.short_name
        form.description.data = project.description
        form.status.data = project.status
        
        users = User.objects(project=project.pk).values_list('pk')
        if users:
            form.participants.data = users

        return render_template('core/projects/project.html', add_project=add_project,
                               form=form, title="Edit Project")


# TODO: Check cascade delete 
# Admin: delete project
@project.route('/projects/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    if not is_admin():
        abort(403)
    else:
        project = Project.objects(pk=id).first()
        linked_tasks = Task.objects(project=project.pk)
        linked_users = User.objects(project=project.pk)

        for task in linked_tasks:
            task.delete()

        for user in linked_users:
            user.project = None
            user.save()
            
        project.delete()
        flash('You have successfully deleted the project.')

        return redirect(url_for('project.list_projects'))
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
