#!/usr/bin/env python3
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
from wtforms.validators import (InputRequired, Email, EqualTo)
from app.models import User


class LoginForm(Form):
    """
    """
    email = StringField('Email', validators=[
        InputRequired(message="Please enter an email address."), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(message="Please enter a password.")])
    remember_me = BooleanField("Remember me.")
    submit = SubmitField("Login")

    def validate(self):
        if not super().validate():
            return False
        else:
            user = User.get(email=self.email.data.lower().strip())

            if user and user.check_password(self.password.data):
                return True
            else:
                self.password.errors.append("Invalid password.")
            return False


class RegisterUserForm(Form):
    firstname = StringField('First Name', validators=[
        InputRequired(message="Please your firstname.")])
    lastname = StringField('Last Name', validators=[
        InputRequired(message="Please your lastname.")])
    email = StringField('Email', validators=[
        InputRequired(message="Please enter an email address."), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(message="Please enter a password."),
        EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Confirm Pasword', validators=[
        InputRequired(message="Please enter a password again.")])
    # recaptcha = StringField('First Name', validators=[ ])
    submit = SubmitField('Register')

    def validate(self):
        """
        """
        if not super().validate():
            return False
        else:
            user = User.get(email=self.email.data.lower().strip())

            if user:
                self.email.errors.append("That email already exists.")
                return False
            else:
                return True


class ForgotPasswordForm(Form):
    email = StringField('Email', validators=[
        InputRequired(message="Please enter an email address."), Email()])
    submit = SubmitField('Send Reset Email')


class ResetPasswordForm(Form):
    password = PasswordField('Password', validators=[
        InputRequired(message="Please enter a password."),
        EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Confirm Pasword', validators=[
        InputRequired(message="Please enter a password again.")])
    submit = SubmitField('Reset Password')
