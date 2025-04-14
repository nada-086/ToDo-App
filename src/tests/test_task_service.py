import unittest
from app import create_app, db
from app.services.task import TaskService
from app.models.task import Task
from app.models.user import User
from datetime import datetime
from flask_login import login_user


class TaskServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.task_service = TaskService(db)

        # Add a test user
        self.user = User(name="Test User", email="test@example.com", password="testpass")
        db.session.add(self.user)
        db.session.commit()

        # Log in the test user
        with self.app.test_request_context():
            login_user(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_task(self):
        self.task_service.create(
            title="Test Task",
            description="Test Description",
            user_id=self.user.id,
            due_date="2024-09-30"
        )
        task = Task.query.filter_by(title="Test Task").first()
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Task")


    def test_update_task(self):
        task = Task(title="Old Task", description="Old Desc",
                    user_id=self.user.id, due_date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()

        self.task_service.update(task, "New Task", "New Desc", "2024-09-30")
        updated_task = Task.query.get(task.id)
        self.assertEqual(updated_task.title, "New Task")
        self.assertEqual(updated_task.description, "New Desc")


    def test_delete_task(self):
        task = Task(title="To Delete", description="Task to delete", user_id=self.user.id, due_date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()

        self.task_service.delete(task)
        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)

    def test_toggle_task_status(self):
        task = Task(title="Complete Task", description="Task to complete",
                    user_id=self.user.id, due_date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()

        self.task_service.toggle_status(task)
        completed_task = Task.query.get(task.id)
        self.assertTrue(completed_task.completed)

        self.task_service.toggle_status(task)
        self.assertFalse(Task.query.get(task.id).completed)