#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.utils
~~~~~~~~~~~~~~~~~

Misc utilities for use throughout the application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from itsdangerous import (URLSafeSerializer, URLSafeTimedSerializer)
from functools import wraps
from flask.ext.login import current_user
from flask import flash, redirect, url_for
from threading import Thread
# from config import ADMINS
from flask.ext.mail import Message
# from app import mail


ADMINS = 'cldershem@gmail.com'
SECRET_KEY = "WHY CANT I IMPORT A CONFIG?!?!!?!"


def format_datetime(date, dt_format='%Y-%m-%d'):
    return date.strftime(dt_format)


def serializer(secret_key=None):
    if secret_key is None:
        secret_key = SECRET_KEY
    return URLSafeSerializer(secret_key)


def timed_serializer(secret_key=None):
    if secret_key is None:
        secret_key = SECRET_KEY
    return URLSafeTimedSerializer(secret_key)


def anon_required(func):
    """
    Decorator that is the antithesis of @login_required.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            flash("Please logout to use this feature.")
            return redirect(url_for('main.index'))
        else:
            return func(*args, **kwargs)
    return wrapper


def async(func):
    """
    Enables process to run in the background while page is loaded.
    """
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


@async
def send_async_email(message):
    """
    """
    # from app import app
    # with app.app_context():
    # mail.send(message)
    pass


def send_email(subject, recipients, text_body, html_body, sender=ADMINS[0]):
    """
    """
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    send_async_email(message)
    return True
