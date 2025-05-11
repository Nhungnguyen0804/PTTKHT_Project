from flask import Blueprint

eventReport_blueprint = Blueprint('eventReport', __name__, template_folder='templates')

from . import routes
