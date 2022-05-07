from crypt import methods
import json
from app import db
from app.models.helper import validate_task
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# CREATE TASK
@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()

    try:
        new_task = Task.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_json()}), 201


# GET ALL TASKS
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("is_complete")

    if title_query:
        tasks = Task.query.filter_by(title = title_query)
    elif description_query:
        tasks = Task.query.filter_by(description = description_query)
    elif completed_query:
        tasks = Task.query.filter_by(is_complete = completed_query)
    else:
        tasks = Task.query.all()  

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200


# GET ONE TASK
@tasks_bp.route("/<id>", methods = ["GET"])
def get_one_task(id):
    task = validate_task(id)
    return jsonify({"task":task.to_json()}), 200

# UPDATE ONE TASK
@tasks_bp.route("/<id>", methods = ["PUT"])
def update_task(id):
    task = validate_task(id) # can i make this a global variable?

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return jsonify({"task":task.to_json()}), 200

# DELETE
@tasks_bp.route("/<id>", methods = ["DELETE"])
def delete_task(id):
    task = validate_task(id) # can i make this a global variable?

    db.session.delete(task)
    db.session.commit()
        
    return jsonify({"details":f'Task {id} "{task.to_json()["title"]}" successfully deleted'}), 200