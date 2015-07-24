from flask import Blueprint


api = Blueprint('api', __name__, url_prefix='/api/v1',
                template_folder='../templates/main')

from . import controller, errors  # nopep8
