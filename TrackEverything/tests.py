import os
import unittest
from datetime import datetime
from flask import abort, url_for
from flask_testing import TestCase
from TrackEverything import create_app, db
from TrackEverything.models import User, Project, Task
from config import TestConfig


class TestBase(TestCase):
    # Test config
    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        return app

    # Before test
    def setUp(self):
        admin = User(first_name="admin_first_name", last_name="admin_last_name", email='admin@admin.com',
                     position=8, username="admin", is_admin=True)
        admin.password = "123"

        user = User(first_name="client_first_name", last_name="client_last_name", email='client@client.com',
                    position=1, username="client", is_admin=False)
        user.password = "123"

        admin.save()
        user.save()

    # After test
    # TODO: Move db-name to config
    def tearDown(self):
        db.connection.drop_database('test')


# TODO: Think about relationships
class TestModels(TestBase):
    def test_user_model(self):
        self.assertEqual(User.objects.count(), 2)

    def test_project_model(self):
        project = Project(name="Test Project", short_name='Test project short_name', status=2,
                          description="Test project description")
        project.save()

        self.assertEqual(Project.objects.count(), 1)

    def test_task_model(self):
        task = Task(name="Test_task", description="Test task description", status=2, start_date=datetime.utcnow)
        task.save()

        self.assertEqual(Task.objects.count(), 1)

    def test_idk(self):
        user = User.objects(first_name="admin_first_name").first()
        task1 = Task(name="Test_task", description="Test task description", status=2, start_date=datetime.utcnow, performers=[user.pk])
        task1.save()

        task2 = Task(name="Test_task2", description="Test task description2", status=2, start_date=datetime.utcnow)
        task2.save()

        user.tasks.append(task1.pk)
        user.save()

        return 


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

    # Test dashboard page
    def test_index_view(self):
        target_url = url_for('index')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test project-list page
    def test_departments_view(self):
        target_url = url_for('api.list_projects')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test tasks-list page
    def test_tasks_view(self):
        target_url = url_for('api.list_tasks')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # Test users-list page
    def test_users_view(self):
        target_url = url_for('api.list_users')
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


if __name__ == '__main__':
    unittest.main()
