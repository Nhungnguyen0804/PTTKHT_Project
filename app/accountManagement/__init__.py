from flask import Blueprint

accManagement_blueprint = Blueprint('accountManagement', __name__, template_folder='templates')

from . import routes
