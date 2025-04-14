# tests/test_user_service.py

import pytest
from app import create_app, db
from app.models.user import User
from app.services.user import UserService
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create a Flask application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    # Use in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()  # Create database tables
        yield app
        db.drop_all()  # Clean up database after tests


@pytest.fixture
def user_service(app):
    """Provide the UserService instance for tests."""
    return UserService(db)


@pytest.fixture
def test_user(app):
    """Create a test user."""
    user = User(
        name='Test User',
        email='test@example.com',
        password=generate_password_hash('testpassword')
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return user


def test_login_success(user_service, test_user):
    """Test user login with valid credentials."""
    result = user_service.login('test@example.com', 'testpassword')
    assert result is True


def test_login_failure(user_service, test_user):
    """Test user login with invalid credentials."""
    result = user_service.login('test@example.com', 'wrongpassword')
    assert result is False


def test_signup_success(user_service):
    """Test user signup with unique email."""
    result = user_service.signup('New User', 'new@example.com', 'newpassword')
    assert result is not None
    assert result.name == 'New User'
    assert result.email == 'new@example.com'


def test_signup_email_already_exists(user_service, test_user):
    """Test user signup with an already registered email."""
    result = user_service.signup(
        'Another User', 'test@example.com', 'anotherpassword')
    assert result is None


def test_get_user_by_email(user_service, test_user):
    """Test retrieving user by email."""
    user = user_service.get_user_by_email('test@example.com')
    assert user is not None
    assert user.name == 'Test User'