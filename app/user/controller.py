#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.users.controller
~~~~~~~~~~~~~~~~~

Controller for User blueprint.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import (render_template, url_for, request, redirect, flash, g,
                   abort, session)
from app import lm
from .forms import (LoginForm, RegisterUserForm, ForgotPasswordForm,
                    ResetPasswordForm)
from . import user
from app.models import User, Debt
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)
from app.utils import anon_required
import datetime


@lm.user_loader
def load_user(user_id):
    user = User.get(email=user_id)
    return user


@user.before_request
def before_request():
    g.user = current_user


@user.route('/login', methods=['GET', 'POST'])
@anon_required
def login():
    form = LoginForm()
    page_title = 'Login'

    if request.method == 'GET':
        return render_template('user_action.html', form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        if form.validate():
            user = User.get(email=form.email.data.lower().strip())
            if user.confirmed and user.is_active:
                login_user(user)
                user.last_seen = datetime.datetime.utcnow()
                user.save()
                return redirect(request.args.get('next') or
                                url_for('.profile', user_id=user.get_id()))
            else:
                flash("Please confirm your email.")
                return render_template('user_action.html', form=form,
                                       page_title=page_title)
        else:
            flash("Form didn't validate.")
            return render_template('user_action.html', form=form,
                                   page_title=page_title)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You've been logged out.")
    return redirect(url_for('main.index'))


@user.route('/register', methods=['GET', 'POST'])
@anon_required
def register():
    form = RegisterUserForm()
    page_title = 'Register'

    if request.method == 'GET':
        return render_template('user_action.html', form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        if form.validate():
            new_user = User(
                firstname=form.firstname.data.title(),
                lastname=form.lastname.data.title(),
                email=form.email.data.lower().strip(),
                password=form.password.data,
                )
            new_user = User.create(new_user)
            flash("Form all good.")
            flash("Registered {}.".format(new_user.email))
            flash("Please confirm your email address by checking your email.")
            return redirect(url_for('.login'))
        else:
            flash("Form didn't validate.")
            return render_template('user_action.html', form=form,
                                   page_title=page_title)


@user.route('/activate/<payload>')
@anon_required
def activate_user(payload):
    user_email = User.check_activation_link(payload)
    if not user_email:
        return abort(404)
    user = User.get(email=user_email)
    if user:
        if not user.confirmed:
            user.activate()
            user.save()
            flash('Your account has been activated.')
        else:
            flash('Your account was already active.')
        return redirect(url_for('.login'))
    else:
        return abort(404)


@user.route('/forgotpassword', methods=['GET', 'POST'])
@anon_required
def forgot_password():
    form = ForgotPasswordForm()
    page_title = 'Forgot Password'

    if request.method == 'GET':
        return render_template('user_action.html',
                               form=form,
                               page_title=page_title)
    elif request.method == 'POST':
        if form.validate():
            user = User.get(email=form.email.data.lower().strip())
            if not user:
                flash("That email does nto exist, please try again.")
                return render_template('user_action.html',
                                       form=form,
                                       page_title=page_title)

            payload = User.get_password_reset_link(user)
            User.email_password_reset(user, payload)
            flash("Password reset email has been sent.  " +
                  "Link expires in 24 hours.")
            return redirect(url_for('main.index'))
        else:
            return render_template('user_action.html',
                                   form=form,
                                   page_title=page_title)


@user.route('/resetpassword/<payload>', methods=['GET', 'POST'])
@anon_required
def reset_password(payload):
    form = ResetPasswordForm()
    page_title = 'Reset Password'
    user, payload_hash = User.check_password_reset_link(payload)

    if request.method == 'GET':
        if not user:
            flash("Token incorrect or has expired.  Please try again.")
            return redirect(url_for('.forgot_password'))
        elif user and payload_hash != user.password[:10]:
            flash("Token has been previously used.  Please try again.")
            return redirect(url_for('.forgot_password'))
        else:
            return render_template('user_action.html',
                                   form=form,
                                   page_title=page_title)

    elif request.method == 'POST':
        if form.validate():
            user.password = form.password.data
            user.save()
            # email "Your password was just reset."
            flash("Password has been reset, please login.")
            return redirect(url_for('.login'))
        else:
            return render_template('user_action.html',
                                   form=form,
                                   page_title=page_title)


@user.route('/profile/<user_id>')
def profile(user_id):
    user = User.get(email=user_id)
    data = Debt.get(to_whom=user.user_id)
    page_title = "{}'s profile".format(user.email)
    return render_template('profile.html', user=user,
                           page_title=page_title, data=data)
