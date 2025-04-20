from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import exams, subjects, questions, user_progress
