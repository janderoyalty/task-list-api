from app import db
from app.routes.helper import validate_task
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request
import requests
import os

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")