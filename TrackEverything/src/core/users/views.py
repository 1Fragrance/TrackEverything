from datetime import datetime

from bson import ObjectId
from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.common.messages import (USER_BANNED_MESSAGE, USER_EDITED_MESSAGE,
                                 USER_RESTORED_MESSAGE)
from src.models import POSITION_CHOICES, USER_STATUS_CHOICES
from src.models.project import Project
from src.models.task import Task
from src.models.user import User

from ..views import is_admin
from . import user
from .forms import UserAssignForm

"""

Fill form projects and tasks
"""
def fill_form_project_and_tasks(form):
    projects = Project.objects().values_list('pk', 'name')

    if projects:
        for project in projects:
            form.project.choices.append((project[0], project[1]))

        selected_project = projects[0][0]
        project_tasks = Task.objects(
            project=selected_project).values_list('pk', 'name')
        for task in project_tasks:
            form.tasks.choices.append((task[0], task[1]))


"""

Show user info endpoint
"""
@user.route('/users/<string:id>')
@login_required
def get_user(id):
    if current_user.id == ObjectId(id) or is_admin():
        user = User.objects(pk=id).first()
        if not user:
            abort(404)

        user_tasks = Task.objects(performer=user.pk)

        if user_tasks:
            user.tasks = user_tasks

        return render_template('core/users/user_info.html',
                               user=user, positions=POSITION_CHOICES, user_statuses=USER_STATUS_CHOICES,
                               title=user.username)
    else:
        abort(403)


"""

Admin: Show all users endpoint
"""
@user.route('/users')
@login_required
def list_users():
    if not is_admin():
        abort(403)
    else:
        users = User.objects().all()
        return render_template('core/users/users.html',
                               users=users, positions=POSITION_CHOICES, user_statuses=USER_STATUS_CHOICES, title='Users')


"""

Admin: change user project/tasks
"""
@user.route('/users/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if is_admin() or current_user.pk == ObjectId(id):
        user = User.objects(pk=id).first()
        if not user:
            abort(404)

        form = UserAssignForm(obj=user)
        fill_form_project_and_tasks(form)

        if request.method == 'POST' and form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.patronymic = form.patronymic.data
            user.position = form.position.data
            user.update_date = datetime.utcnow()
            if form.project.raw_data:
                user.project = ObjectId(form.project.data)
            user.save()

            for old_task in Task.objects(performer=user.pk):
                old_task.update(unset__performer=1)

            Task.objects(pk__in=form.tasks.raw_data).update(
                performer=user.pk)

            flash(USER_EDITED_MESSAGE)
            return redirect(url_for('user.get_user', id=user.pk))

        form.username = user.username
        form.email = user.email
        form.first_name = user.first_name
        form.last_name = user.last_name
        form.patronymic = user.patronymic
        form.position = user.position
        if user.project:
            form.project = str(user.project)

        tasks = Task.objects(performer=user.pk).values_list('pk')
        if tasks:
            form.tasks.data = tasks

        return render_template('core/users/user.html',
                               user=user, form=form,
                               title='Edit User')
    else:
        abort(403)


"""

Ban user endpoint
"""
@user.route('/users/ban/<string:id>', methods=['GET', 'POST'])
@login_required
def ban_user(id):
    if not is_admin() or current_user.pk == ObjectId(id):
        abort(403)
    else:
        user = User.objects(pk=id).first()
        if not user:
              abort(404)
        user.status = 2
        user.update_date = datetime.utcnow()
        user.save()
        flash(USER_BANNED_MESSAGE)

        return redirect(url_for('user.list_users'))


"""

Restore user endpoint
"""
@user.route('/users/restore/<string:id>', methods=['GET', 'POST'])
@login_required
def restore_user(id):
    if not is_admin() or current_user.pk == ObjectId(id):
        abort(403)
    else:
        user = User.objects(pk=id).first()
        if not user:
            abort(404)
        user.status = 1
        user.update_date = datetime.utcnow()
        user.save()
        flash(USER_RESTORED_MESSAGE)

        return redirect(url_for('user.list_users'))
