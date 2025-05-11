from flask import Blueprint, render_template
from app.models.post import Post
from app.models.category import Category
home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
@home_blueprint.route('/home')
def homepage():
    posts = Post.query.filter_by(is_approved=True, status='Not done').all()
    categorys = Category.query.all()
    return render_template('home/home.html', posts=posts,categorys =categorys)



@home_blueprint.context_processor
def inject_categories():
    from app.models.category import Category
    return dict(categorys=Category.query.all())