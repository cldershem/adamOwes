#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py
~~~~~~~~~~~~~~~~~

This is an application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from .utils import format_datetime
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from celery import Celery


db = SQLAlchemy()
bcrypt = Bcrypt()
lm = LoginManager()
mail = Mail()
celery = Celery('app')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    lm.init_app(app)
    lm.login_view = "user.login"
    bcrypt.init_app(app)
    mail.init_app(app)
    create_celery_app(app, celery)

    app.jinja_env.filters['format_datetime'] = format_datetime

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .main import main as main_module
    from .api import api as api_module
    from .user import user as user_module
    from .debt import debt as debt_module

    app.register_blueprint(main_module)
    app.register_blueprint(api_module)
    app.register_blueprint(user_module)
    app.register_blueprint(debt_module)

    return app


def create_celery_app(app, celery):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
