from flask import Blueprint, render_template, request
from app.models.post import Post
from app.models.category import Category
home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
@home_blueprint.route('/home')
def homepage():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Post.query.filter_by(is_approved=True, status='Not done')
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    start = (page - 1) * per_page + 1
    end = min(start + per_page - 1, pagination.total)

    return render_template(
        'home/home.html',
        posts=posts,
        categorys=Category.query.all(),
        pagination=pagination,
        start=start,
        end=end
    )

@home_blueprint.context_processor
def inject_categories():
    from app.models.category import Category
    return dict(categorys=Category.query.all())