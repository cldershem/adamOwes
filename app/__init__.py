#!/usr/bin/env python
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
from utils import format_datetime


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.jinja_env.filters['format_datetime'] = format_datetime

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from main import main as main_module
    from api.controller import mod as api_module

    app.register_blueprint(main_module)
    app.register_blueprint(api_module)

    return app
