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
    APP_NAME = "Adam Owes"
    CSRF_ENABLED = True
    SECRET_KEY = secrets.SECRET_KEY
    UPLOAD_DIR = os.path.join(BASE_DIR, 'app/static/img/uploads/')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('adamOwes', 'cldershem@gmail.com')
    MAIL_USERNAME = secrets.MAIL_USERNAME
    MAIL_PASSWORD = secrets.MAIL_PASSWORD
    CELERY_BROKER_URL = 'amqp://'
    CELERY_RESULT_BACKEND = 'amqp://'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(BASE_DIR, 'tmp/dev.sqlite'))


class TestingConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(BASE_DIR, 'tmp/test.sqlite'))


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(BASE_DIR, 'tmp/production.sqlite'))


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    }
