#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.users.controller
~~~~~~~~~~~~~~~~~

Controller for Users blueprint.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import (render_template, url_for, request, redirect,
                   flash, g, abort, session)
from app import lm
from .forms import (LoginForm, RegisterUserForm, ForgotPasswordForm,
                    ResetPasswordForm)
from . import user
from app.models import User
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)
# from app.utils import anon_required


@lm.user_loader
def load_user(user_id):
    user = User.get(email=user_id)
    return user


@user.before_request
def before_request():
    g.user = current_user


# @anon_required
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    page_title = 'Login'

    if request.method == 'GET':
        return render_template('user_action.html', form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        return render_template('user_action.html', form=form,
                               page_title=page_title)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout'


@user.route('/register', methods=['GET', 'POST'])
# @anon_required
def register():
    form = RegisterUserForm()
    page_title = 'Register'

    if request.method == 'GET':
        return render_template('user_action.html', form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        return render_template('user_action.html', form=form,
                               page_title=page_title)


@user.route('/activate/<payload>')
# @anon_required
def activate_user(payload):
    return 'activate'


@user.route('/forgotpassword', methods=['GET', 'POST'])
# @anon_required
def forgot_password():
    form = ForgotPasswordForm()
    page_title = 'Forgot Password'

    if request.method == 'GET':
        return render_template('user_action.html', form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        return render_template('user_action.html', form=form,
                               page_title=page_title)


@user.route('/resetpassword/<payload>', methods=['GET', 'POST'])
# @anon_required
def reset_password(payload):
    form = ResetPasswordForm()
    page_title = 'Reset Password'

    if request.method == 'GET':
        return render_template('user_action.html', form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        return render_template('user_action.html', form=form,
                               page_title=page_title)


@user.route('/profile/<user_id>')
def profiles(user_id):
    # user = User.get(email=user_id)
    return 'profile'
