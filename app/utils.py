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
from app import config
from functools import wraps
from flask.ext.login import current_user
from flask import flash, redirect, url_for


def format_datetime(date, dt_format='%Y-%m-%d'):
    return date.strftime(dt_format)


def serializer(secret_key=None):
    if secret_key is None:
        secret_key = config.SECRET_KEY
    return URLSafeSerializer(secret_key)


def timed_serializer(secret_key=None):
    if secret_key is None:
        secret_key = config.SECRET_KEY
    return URLSafeTimedSerializer(secret_key)


def anon_required(func):
    """
    Decorator that is the antithesis of @login_required.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            flash("Please logout to use this feature.")
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
        return wrapper
