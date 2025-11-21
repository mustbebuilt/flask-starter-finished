from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', static_url_path='/static/main', static_folder='static')

from . import routes  # Import routes after blueprint is defined