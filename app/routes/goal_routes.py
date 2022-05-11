from app import db
from app.routes.helper import validate_goal
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request
import requests
import os

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# GET ALL GOALS
@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals  = Goal.query.all()
    goals_response = [goal.g_json() for goal in goals]

    return jsonify(goals_response), 200


# GET ONE GOAL
@goals_bp.route("/<id>", methods = ["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    
    return jsonify({"goal": goal.g_json()}), 200


# CREATE GOAL
@goals_bp.route("", methods = ["POST"])
def create_goals():
    request_body = request.get_json()
    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.g_json()}), 201



# UPDATE GOAL - "/tasks/1" - PUT
@goals_bp.route("/<id>", methods = ["PUT"])
def update(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    
    
    goal.update_goal(request_body) 
    # is it better to have update_goal or update?

    db.session.commit()

    return jsonify({"goal": goal.g_json()}), 200


# DELETE GOAL - "/tasks/1" - DELTE
@goals_bp.route("/<id>", methods = ["DELETE"])
def delete(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {id} "{goal.title}" successfully deleted'}), 200





