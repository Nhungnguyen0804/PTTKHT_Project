from flask import Blueprint

report_blueprint = Blueprint('report', __name__, template_folder='templates')

from . import routes
