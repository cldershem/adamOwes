#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.email
~~~~~~~~~~~~~~~~~

Functions involving email.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask.ext.mail import Message
from app import mail
from flask import render_template
# from config import ADMINS
from utils import async


ADMINS = 'cldershem@gmail.com'


@async
def send_async_email(message):
    """
    """
    # from app import app
    # with app.app_context():
    mail.send(message)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    """
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    send_async_email(message)
    return True


def email_confirmation(user, payload):
    """
    """
    send_email("[adamOwes] - confirm email",
               ADMINS,
               [user.email],
               render_template("emails/email_confirmation.txt",
                               user=user, payload=payload),
               render_template("emails/email_confirmation.html",
                               user=user, payload=payload))

    return True


def email_password_reset(user, payload):
    """
    """
    send_email("[adamOwes] - password reset",
               ADMINS,
               [user.email],
               render_template("emails/password_reset.txt",
                               user=user,
                               payload=payload),
               render_template("emails/pasword_reset.html",
                               user=user,
                               payload=payload))

    return True
