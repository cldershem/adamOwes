#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
config.py
~~~~~~~~~~~~~~~~~

Config for application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/$SOME_REPO
"""
import secrets
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "SOME APP NAME"
    CSRF_ENABLED = True
    SECRET_KEY = secrets.SECRET_KEY
    UPLOAD_DIR = os.path.join(BASE_DIR, 'app/static/img/uploads/')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(BASE_DIR, 'tmp/dev.sqlite'))


class TestingConfig(Config):
    Testing = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    }
