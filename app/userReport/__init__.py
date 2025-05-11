from flask import Blueprint

userReport_blueprint = Blueprint('userReport', __name__, template_folder='templates')

from . import routes
