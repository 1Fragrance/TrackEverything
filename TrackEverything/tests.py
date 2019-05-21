import unittest
from datetime import datetime
from flask import abort, url_for
from flask_testing import TestCase
from src import create_app, db
from src.models.user import User
from src.models.project import Project
from src.models.task import Task
from src.core.projects.forms import ProjectForm
from src.core.users.forms import UserAssignForm
from src.core.tasks.forms import TaskForm
from bson import ObjectId


class TestBase(TestCase):
    # TODO: Move config_name to config_file
    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        return app

    # Before test
    def setUp(self):
        admin = User(first_name="admin_first_name", last_name="admin_last_name", email='admin@admin.com',
                     position=8, username="admin", is_admin=True, status=1)
        admin.password = "123"

        user = User(first_name="client_first_name", last_name="client_last_name", email='client@client.com',
                    position=1, username="client", is_admin=False, status=1)
        user.password = "123"

        admin.save()
        user.save()

    # After test
    # TODO: Move db-name to config
    def tearDown(self):
        db.connection.drop_database('test')

class TestModels(TestBase):
    def test_user_save(self):
        self.assertEqual(User.objects.count(), 2)

    def test_project_save(self):
        project = Project(name="Test Project", short_name='Test project short_name', status=2,
                          description="Test project description")
        project.save()

        self.assertEqual(Project.objects.count(), 1)

    def test_task_save(self):
        task = Task(name="Test_task", description="Test task description", status=2, start_date=datetime.utcnow)
        task.save()
        self.assertEqual(Task.objects.count(), 1)


class TestViews(TestBase):
    # Test login page
    def test_login_view(self):
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    # Test logout page
    def test_logout_view(self):
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test index page
    def test_index_view(self):
        target_url = url_for('core.index')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test project-list page
    def test_departments_view(self):
        target_url = url_for('project.list_projects')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test tasks-list page
    def test_tasks_view(self):
        target_url = url_for('task.list_tasks')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test users-list page
    def test_users_view(self):
        target_url = url_for('user.list_users')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):
    # Test 403 error
    def test_403_forbidden(self):
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)

    # Test 404 error
    def test_404_not_found(self):
        response = self.client.get('/Lorem')
        self.assertEqual(response.status_code, 404)

    # Test 500 error
    def test_500_internal_server_error(self):
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)

class TestAPI(TestBase):
    
    def login_admin(self):
        return self.client.post(url_for('auth.login'), data={'email': 'admin@admin.com',
                                             'password': '123'}, follow_redirects=True)


    def login_user(self):
        return self.client.post(url_for('auth.login'), data={'email': 'client@client.com',
                                                'password': '123'}, follow_redirects=True)
    def test_register(self):
        target_url = url_for('auth.register')
        response = self.client.post(target_url, data={'email': 'test@email.com', 'password':123}, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects(email='test@email.com').first)

    def test_login(self):
        assert self.login_admin().status_code == 200
        assert self.login_user().status_code == 200

    def test_logout(self):
        with self.client:
            assert self.login_user().status_code == 200
            target_url = url_for('auth.logout')
            response = self.client.get(target_url, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_get_projects(self):
        with self.client:
            assert self.login_admin().status_code == 200
            result = self.client.get(url_for('project.list_projects'), follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            
    def test_get_tasks(self):
        with self.client:
            assert self.login_admin().status_code == 200
            result = self.client.get(url_for('task.list_tasks'), follow_redirects=True)
            self.assertEqual(result.status_code, 200)

    def test_get_users(self):
        with self.client:
            assert self.login_admin().status_code == 200
            result = self.client.get(url_for('user.list_users'), follow_redirects=True)
            self.assertEqual(result.status_code, 200)

    def test_add_project(self):
        with self.client:
            assert self.login_admin().status_code == 200
            project = Project(name='test', short_name='test', status=2, description='description')
            form = ProjectForm(formdata=None, obj=project)
            result = self.client.post(url_for('project.add_project'), data=form.data, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            assert Project.objects(name='test').first() is not None

    def test_add_task(self):
        with self.client:
            assert self.login_admin().status_code == 200
            task = Task(name='test', status=2, description='descr', start_date=datetime.now())
            form = TaskForm(formdata=None, obj=task)
            result = self.client.post(url_for('task.add_task'), data=form.data, follow_redirects=True)
            print(result.data)
            self.assertEqual(result.status_code, 200)
            assert Task.objects(name='test').first() is not None

    def test_edit_task(self):
        with self.client:
            assert self.login_admin().status_code == 200
            task = Task(name='test', status=2, description='descr', start_date=datetime.now())
            form = TaskForm(formdata=None, obj=task)
            result = self.client.post(url_for('task.add_task'), data=form.data, follow_redirects=True)
            self.assertEqual(result.status_code, 200)

            task_db = Task.objects(name='test').first()
            assert task_db is not None
            task_db.name='new_name'
            form = TaskForm(formdata=None, obj=task_db)
            result = self.client.post(url_for('task.edit_task'), data=form.data, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            assert Task.objects(name='new_name').first() is not None

if __name__ == '__main__':
    unittest.main()
