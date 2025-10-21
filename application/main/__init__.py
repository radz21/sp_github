from flask import Blueprint, session

main = Blueprint('main', __name__)
from . import routes
from . import routes_queries





