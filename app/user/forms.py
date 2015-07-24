#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.users.forms
~~~~~~~~~~~~~~~~~

Forms needed for the `Users` Blueprint.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask_wtf import Form
from wtforms import (StringField, SubmitField, PasswordField, BooleanField)
from wtforms.validators import (InputRequired, Email)


class LoginForm(Form):
    """
    """
    email = StringField('Email', validators=[
        InputRequired(message="Please enter an email address."), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(message="Please enter a password.")])
    remember_me = BooleanField("Remember me.")
    submit = SubmitField("Login")


class RegisterUserForm(Form):
    firstname = StringField('First Name', validators=[
        InputRequired(message="Please your firstname.")])
    lastname = StringField('Last Name', validators=[
        InputRequired(message="Please your lastname.")])
    email = StringField('Email', validators=[
        InputRequired(message="Please enter an email address."), Email()])
    password = StringField('First Name', validators=[
        InputRequired(message="Please enter a password.")])
    confirm = StringField('First Name', validators=[
        InputRequired(message="Please enter a password again.")])
    # recaptcha = StringField('First Name', validators=[ ])
    submit = StringField('Register')


class ForgotPasswordForm(Form):
    email = StringField('Email', validators=[
        InputRequired(message="Please enter an email address."), Email()])
    submit = StringField('Send Reset Email')


class ResetPasswordForm(Form):
    password = StringField('First Name', validators=[
        InputRequired(message="Please enter a password.")])
    confirm = StringField('First Name', validators=[
        InputRequired(message="Please enter a password again.")])
    submit = StringField('Register')
