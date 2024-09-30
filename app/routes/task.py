from flask import Blueprint, request, render_template, redirect
from flask_injector import inject
from flask_login import current_user
from app.services.task import TaskService

task = Blueprint("task", __name__)


@task.route('/')
@inject
def list_task(task_service: TaskService):
    tasks = task_service.get_tasks(current_user.id)
    return render_template('./task/list.html', tasks=tasks)


@task.route('/create')
def create_task():
    return render_template("./task/create.html")


@task.route('/create', methods=['POST'])
@inject
def store_task(task_service: TaskService):
    print("Entered")
    task_title = request.form.get('title')
    task_date = request.form.get('due-date')
    task_description = request.form.get('description')

    if not task_title:
        return render_template('./task/create.html', message="All Fields are Required.")

    print("Passed")
    try:
        task_service.create(title=task_title, description=task_description, user_id=current_user.id, due_date=task_date)
    except Exception as e:
        print("Exception: " + str(e))
        return render_template('./task/create.html', message=str(e))
    return redirect('/tasks')


@task.route('/<id>')
@inject
def view_task(task_service: TaskService, id):
    task = task_service.get_by_id(id)
    if not task:
        return redirect('/tasks')
    return render_template('./task/view.html', task=task)


@task.route('/<id>/edit')
@inject
def edit_task(task_service: TaskService, id):
    task = task_service.get_by_id(id)
    if not task:
        return redirect('/tasks')
    return render_template('./task/edit.html', task=task)


@task.route('/<id>', methods=['POST'])
@inject
def update_task(task_service: TaskService, id):
    task = task_service.get_by_id(id)
    if not task:
        return render_template('./task/view.html', message="Page Not Found")

    task_title = request.form.get('title')
    task_description = request.form.get('description')
    task_due_date = request.form.get('due-date')

    if not task:
        return render_template('./task/view.html', task=task, message="Enter a Unique Title")

    task_service.update(task, task_title, task_description, task_due_date)
    return render_template('./task/view.html', task=task)


@task.route('/<id>/delete')
@inject
def delete_task(task_service: TaskService, id):
    task = task_service.get_by_id(id)
    if not task:
        return redirect('/tasks')
    task_service.delete(task)
    return redirect('/tasks')

@task.route('/<id>/toggle-status')
@inject
def toggle_status(task_service: TaskService, id):
    task = task_service.get_by_id(id)
    if not task:
        return redirect('/tasks')
    task_service.toggle_status(task)
    return redirect(f'/tasks/{task.id}')

@task.route('/search', methods=['POST'])
@inject
def search(task_service: TaskService):
    topic = request.form.get('search')
    tasks = task_service.get_by_topic(topic)
    print(tasks)
    return render_template('./task/list.html', tasks=tasks)