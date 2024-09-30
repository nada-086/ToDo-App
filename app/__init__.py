from flask import Flask, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    # Create Flask Application
    app = Flask(__name__)

    # Load the Configuration
    app.config.from_object(Config)

    # Initialize the correct database based on configuration
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Import and register blueprints inside the function to avoid circular imports
    from app.routes.task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix="/tasks")
    from app.routes.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")

    # Rendering the Home Page
    @app.route('/')
    def home():
        return redirect('/user/login')

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(user_id)
    return app