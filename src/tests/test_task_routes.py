from flask_injector import FlaskInjector, singleton
import pytest
from datetime import datetime
from flask import url_for
from app import create_app, db
from app.models.task import Task
from app.models.user import User
from flask_login import login_user

from app.services.task import TaskService
from app.services.user import UserService


@pytest.fixture
def app():
    app = create_app()

    def configure_test_injector(binder):
        # Use mock services here or bind to actual services depending on the test.
        binder.bind(UserService, to=UserService(db), scope=singleton)
        binder.bind(TaskService, to=TaskService(db), scope=singleton)

    with app.app_context():
        db.create_all()
        # Configure the injector for tests
        FlaskInjector(app=app, modules=[configure_test_injector])
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def login_user_fixture(app, client):
    # Create a user for login
    with app.app_context():
        user = User(name="testuser", email='testuser@gmail.com',
                    password='password1234')
        db.session.add(user)
        db.session.commit()

        # Log in the user using Flask-Login
        login_user(user)  # Directly log in the user
        yield client

# Test the add task with a valid input
def test_add_task_with_valid_input(login_user_fixture):
    response = login_user_fixture.post('/tasks/create', data={
        'title': 'Valid Task',
        'due-date': '2024-10-01',
        'description': 'This is a valid task description.'
    })
    assert response.status_code == 302
    assert Task.query.count() == 1

# Test the add task with an empty title which is invalid
def test_add_task_with_invalid_input(login_user_fixture):
    response = login_user_fixture.post('/tasks/create', data={
        'title': '',
        'due-date': '2024-10-01',
        'description': 'This task has no title.'
    })
    assert response.status_code == 400 
    assert Task.query.count() == 0

# Test the add task with an wrong date formate which is wrong
def test_add_task_with_invalid_input(login_user_fixture):
    response = login_user_fixture.post('/tasks/create', data={
        'title': '',
        'due-date': '2222222222',
        'description': 'This task has no title.'
    })
    assert response.status_code == 400
    assert Task.query.count() == 0

# Test marking a task as completed
def test_mark_task_as_complete(login_user_fixture):
    task = Task(title='Complete Me', description='This task will be completed.',
                due_date=datetime(2024, 10, 1), user_id=1)
    db.session.add(task)
    db.session.commit()

    response = login_user_fixture.get(f'/tasks/{task.id}/toggle-status')
    assert response.status_code == 302
    task = Task.query.get(task.id)
    assert task.completed is True

# Test case for deleting a task
def test_delete_task(login_user_fixture):
    task = Task(title='Delete Me', description='This task will be deleted.',
                due_date=datetime(2024, 10, 1), user_id=1)
    db.session.add(task)
    db.session.commit()

    response = login_user_fixture.get(f'/tasks/{task.id}/delete')
    assert response.status_code == 302
    assert Task.query.count() == 0 

# Test case for deleting a non existing task
def test_delete_not_existing_task(login_user_fixture):
    response = login_user_fixture.get(f'/tasks/1/delete')
    assert response.status_code == 400
    assert Task.query.count() == 0

# Boundary Testing: Task name length
def test_add_task_with_long_title(login_user_fixture):
    long_title = 'A' * 201
    response = login_user_fixture.post('/tasks/create', data={
        'title': long_title,
        'due-date': '2024-10-01',
        'description': 'This task has a long title.'
    })
    assert response.status_code == 400


# Test toggling the task status
def test_task_state_transition(login_user_fixture):
    task = Task(title='State Transition Test', description='Initial state test.',
                due_date=datetime(2024, 10, 1), user_id=1)
    db.session.add(task)
    db.session.commit()

    assert task.completed == False
    response = login_user_fixture.get(
        url_for('task.toggle_status', id=task.id))
    task = Task.query.get(task.id)
    assert task.completed == True

# Test editing a valid task
def test_edit_task_with_valid_id(login_user_fixture):
    task = Task(title='Edit Me', description='This task is for editing.',
                due_date=datetime(2024, 10, 1), user_id=1)
    db.session.add(task)
    db.session.commit()

    response = login_user_fixture.get(f'/tasks/{task.id}/edit')
    assert response.status_code == 302


# Test editing a non existing task
def test_edit_task_with_invalid_id(login_user_fixture):
    response = login_user_fixture.get('/tasks/9999/edit')
    assert response.status_code == 400
