from flask import Blueprint

# Khởi tạo blueprint
post_blueprint = Blueprint('post', __name__, template_folder='templates')

# Import routes sau khi tạo blueprint để tránh vòng lặp
from . import post_routes

print(">> Post blueprint initialized")
