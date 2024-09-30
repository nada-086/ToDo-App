from flask import Blueprint, render_template, redirect, request
from flask_injector import inject
from flask_login import logout_user
from app.services.user import UserService

user = Blueprint("user", __name__)


@user.route('/')
def home():
    return redirect('/')


@user.route('/login', methods=['GET'])
def login_form():
    return render_template("./user/login.html")


@user.route('/login', methods=['POST'])
@inject
def login(user_service: UserService):
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return render_template("./user/login.html", message="All Fields are Required.")

    status = user_service.login(email=email, password=password)
    if not status:
        return render_template('./user/login.html', message="Please, Enter a Valid Username and Password.")
    return redirect('/tasks')


@user.route('/signup', methods=['GET'])
def signup_form():
    return render_template("./user/signup.html")


@user.route('/signup', methods=['POST'])
@inject
def signup(user_service: UserService):
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        return render_template("./user/signup.html", message="All Fields are Required.")

    if user_service.get_user_by_email(email=email):
        return render_template('./user/signup.html', message="Email is Already Registered. Try to Log In.")

    user_created = user_service.signup(name=name, email=email, password=password)
    if not user_created:
        return render_template('/user/signup.html', message="Failed to create the user. Please try again.")

    return redirect('/user/login')

@user.route('/logout')
def logout():
    logout_user()
    return redirect('/user/login')
