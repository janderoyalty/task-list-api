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
        if request_body["title"] or request_body["description"]:
            new_task = Task.create(request_body)
        elif request_body["completed_at"]:
            new_task = Task.create_task_complete(request_body)
            # new_task["completed_at"] = Task.datetime.utcnow()

    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_json()}), 201



# GET ALL TASKS
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    # SORT
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
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
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()
        
    return jsonify({"details":f'Task {id} "{task.to_json()["title"]}" successfully deleted'}), 200

# IS MARKED
@tasks_bp.route("/<id>/mark_complete", methods = ["PATCH"])
def mark_completed(id):
    task = validate_task(id) # can i make this a global variable?

    request_body = request.get_json()

    task.patch_complete(request_body)

    db.session.commit()

    return jsonify({"task":task.to_json()}), 200


@tasks_bp.route("/<id>/mark_incomplete", methods = ["PATCH"])
def mark_imcompleted(id):
    task = validate_task(id) # can i make this a global variable?

    request_body = request.get_json()

    task.patch_imcomplete(request_body)

    db.session.commit()

    return jsonify({"task":task.to_json()}), 200

