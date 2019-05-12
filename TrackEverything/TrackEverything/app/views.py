from . import app
from flask import abort, flash, redirect, render_template, url_for, jsonify
from flask_login import current_user, login_required
from .forms import TaskForm, ProjectForm, UserAssignForm
from ..models import Task, Project, User


def is_admin():
    if not current_user.is_admin:
        return False
    return True

@app.route('/')
@login_required
def index():
    return render_template('app/index.html', title="Index page")


# Common part
# Tasks
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def list_tasks():
    if is_admin():
        tasks = Task.objects.all()
    else:
        tasks = Task.objects(performers=current_user.pk)

    return render_template('app/tasks/tasks.html',
                           tasks=tasks, title="Tasks")

@app.route('/projects')
@login_required
def list_projects():
    if is_admin():
        projects = Project.objects.all()
    else:
        projects = Project.objects(participants=current_user.pk)
    return render_template('app/projects/projects.html',
                           projects=projects, title='Projects')


# Admin part
@app.route('/tasks/add', methods=['GET', 'POST'])
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

            return redirect(url_for('app.list_tasks'))

        return render_template('app/tasks/task.html', action="Add", add_task=add_task,
                           form=form, title="Add Task")


# TODO add change status
@app.route('/tasks/edit/<string:id>', methods=['GET', 'POST'])
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

            return redirect(url_for('app.list_tasks'))

        form.name.data = task.name
        form.description.data = task.description
        form.status.data = task.status
        form.start_date.data = task.start_date
        form.end_date.data = task.end_date

        project_users = User.objects(project=task.project).values_list('pk', 'username')
        for user in project_users:
            form.performers.choices.append((user[0], user[1]))

        form.performers.data = task.performers


        return render_template('app/tasks/task.html', action="Edit",
                            add_task=add_task, form=form,
                            task=task, title="Edit Task")


@app.route('/tasks/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    if not is_admin():
        abort(403)
    else:
        # TODO: 404 error validation
        task = Task.objects(pk=id).first()
        task.delete()
        flash('You have successfully deleted the task.')

        return redirect(url_for('app.list_tasks'))
        return render_template(title="Delete Task")


# Project
@app.route('/projects/add', methods=['GET', 'POST'])
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

            return redirect(url_for('app.list_projects'))


        return render_template('app/projects/project.html', add_project=add_project,
                                form=form, title='Add Project')


@app.route('/projects/edit/<string:id>', methods=['GET', 'POST'])
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

            return redirect(url_for('app.list_projects'))

        form.name.data = project.name
        form.short_name.data = project.short_name
        form.description.data = project.description
        form.status.data = project.status

        return render_template('app/projects/project.html', add_project=add_project,
                                form=form, title="Edit Project")


@app.route('/projects/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    if not is_admin():
        abort(403)
    else:
        project = Project.objects(pk=id).first()
        project.delete()
        flash('You have successfully deleted the project.')

        return redirect(url_for('app.list_projects'))
        return render_template(title="Delete Project")


# User 
@app.route('/users')
@login_required
def list_users():
    if not is_admin():
        abort(403)
    else:
        users = User.objects.all()
        return render_template('app/users/users.html',
                                users=users, title='Users')


@app.route('/users/assign/<string:id>', methods=['GET', 'POST'])
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

            return redirect(url_for('app.list_users'))

        return render_template('app/users/user.html',
                                user=user, form=form,
                                title='Assign User')


# ModelsAPI
@app.route('/projects/<project_id>/tasks')
def get_project_tasks(project_id):
    tasks = Task.objects(project=project_id).values_list('pk', 'name')

    tasksArray = []
    
    for task in tasks:
        taskObj = {}
        taskObj['pk'] = str(task[0])
        taskObj['name'] = task[1]
        tasksArray.append(taskObj)
    
    return jsonify({'tasks' : tasksArray})

@app.route('/projects/<project_id>/users')
def get_project_users(project_id):
    users = User.objects(project=project_id).values_list('pk', 'username')

    usersArray = []
    
    for user in users:
        userObj = {}
        userObj['pk'] = str(user[0])
        userObj['username'] = user[1]
        usersArray.append(userObj)
    
    return jsonify({'users' : usersArray})


