from flask import Blueprint, render_template
from app.models.post import Post

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
@home_blueprint.route('/home')
def homepage():
    posts = Post.query.filter_by(is_approved=True, status='Not done').all()
    return render_template('home/home.html', posts=posts)
