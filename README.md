# Task Manager Application

This is a simple **Task Manager** application built using the Flask framework. It allows users to manage tasks through functionalities such as adding, completing, deleting, and searching for tasks. Users can also sign up and log in to secure their tasks.

---

## Features

1. **Add Tasks**: Users can create tasks with a name and description.
2. **Complete Tasks**: Mark tasks as complete.
3. **Delete Tasks**: Remove tasks from the list.
4. **Search Tasks**: Search tasks by keywords in their titles.
5. **User Authentication**:
   - Sign up for a new account.
   - Log in to access task management features securely.

---

## Technologies Used

The project uses the following Python libraries:

### Flask Framework
- **Flask**: Core framework for web application.
- **flask_sqlalchemy**: ORM for database interactions.
- **flask_login**: Handles user authentication and session management.
- **flask_inject**: Dependency injection for better modularity.
- **python_dotenv**: Manage environment variables securely.
- **werkzeug**: Provides utility functions and a secure password hashing system.
- **flask_migrate**: Enables database schema migrations in Flask apps using Alembic with SQLAlchemy.

### Testing
- **pytest**: Framework for unit testing.
- **pytest-flask**: Extension for testing Flask applications.
- **flask_injector**: Integration with Flask for dependency injection.

---

## Project Structure
```
Task Manager
├── app.py              # Entry point for the Flask application
├── models.py           # Database models
├── routes.py           # Application routes
├── templates/          # HTML templates for the UI
├── static/             # Static files (CSS, JS, Images)
├── tests/              # Unit tests for the application
└── .env                # Environment variables
```

---

## Product BackLog
[Figma URL](https://www.figma.com/board/ioMlZPs6OdTUBh5Yqa2uJT/Product-Backlog?node-id=0-1&p=f)
