from app import create_app, db
from flask_injector import FlaskInjector, singleton
from app.services.user import UserService
from app.services.task import TaskService


def configure(binder):
    binder.bind(UserService, to=UserService(db), scope=singleton)
    binder.bind(TaskService, to=TaskService(db), scope=singleton)


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    FlaskInjector(app=app, modules=[configure])
    app.run()