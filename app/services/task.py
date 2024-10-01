from datetime import datetime
from app.models.task import Task
from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from flask_login import current_user


class TaskService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_tasks(self, user_id):
        return self.db.session.query(Task).filter_by(user_id=user_id).all()

    def create(self, title, description, user_id, due_date):
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise Exception("Invalid date format. Please use YYYY-MM-DD.")

        task = self.db.session.query(Task).filter_by(title=title).first()
        if task:
            raise Exception('Please, Choose a Unique Title for Your Task.')

        new_task = Task(title=title, description=description, user_id=user_id, due_date=due_date)
        self.db.session.add(new_task)
        self.db.session.commit()

    def get_by_id(self, id):
        return self.db.session.query(Task).filter_by(id=id).first()

    def update(self, task, title, description, due_date):
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise Exception("Invalid date format. Please use YYYY-MM-DD.")
        print(due_date)
        task.title = title
        task.description = description
        task.due_date = due_date
        self.db.session.commit()

    def delete(self, task):
        self.db.session.delete(task)
        self.db.session.commit()
        
    def toggle_status(self, task):
        task.completed = (not task.completed)
        self.db.session.commit()

    def get_by_topic(self, topic):
        search_query = f"%{topic}%"
        return self.db.session.query(Task) \
            .filter(Task.user_id == current_user.id, Task.title.ilike(search_query)) \
            .all()
