from flask import Blueprint,render_template

test_blueprint = Blueprint('test', __name__, template_folder='templates')

@test_blueprint.route('/test')

def afterlogin():
    return render_template('test/afterlogin.html')
