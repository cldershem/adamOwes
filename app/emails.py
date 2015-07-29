#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.emails
~~~~~~~~~~~~~~~~~

Misc utilities for sending emails.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import current_app  # , flash
from . import mail, celery
from flask.ext.mail import Message


@celery.task
def send_async_email(message):
    """
    """
    with current_app.app_context():
        mail.send(message)


def send_email(subject, recipients, text_body, html_body):
    """
    """
    message = Message(subject, recipients=recipients)
    message.body = text_body
    message.html = html_body
    send_async_email(message)
    return True
