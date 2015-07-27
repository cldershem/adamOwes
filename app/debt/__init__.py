from flask import Blueprint


debt = Blueprint('debt', __name__, url_prefix='/debt',
                 template_folder='../templates/debt')

from . import controller, errors  # nopep8
