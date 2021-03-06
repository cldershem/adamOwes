#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.debt.controller
~~~~~~~~~~~~~~~~~

Controller for Debt blueprint.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import (render_template, request, flash, current_app, redirect,
                   url_for, session)
from app import db
from app.models import Debt  # , Photo
from app.debt.forms import AddNewDebtForm
from . import debt
from werkzeug import secure_filename
from flask.ext.login import (login_required)


@debt.route('/')
def list_debts():
    data = Debt.get()
    return render_template('list.html', data=data)


@debt.route('/add', methods=['GET', 'POST'])
@login_required
def add_new():
    form = AddNewDebtForm()

    if request.method == 'GET':
        return render_template('add_new.html', form=form)
    if request.method == 'POST':
        if not form.validate():
            flash("Form didn't validate.")
            return render_template('add_new.html', form=form)
        else:
            new_debt = Debt(
                debt_type=form.debt_type.data,
                description=form.description.data,
                amount=form.amount.data,
                to_whom=form.to_whom.data,
                debt_date=form.debt_date.data,
                compound_frequency=form.compound_frequency.data,
                )
            if form.interest.data:
                new_debt.interest = form.interest.data
            if form.fees.data:
                new_debt.fees = form.fees.data
            if form.photo.data:
                filename = secure_filename(form.photo.data.filename)
                form.photo.data.save(
                    current_app.config['UPLOAD_DIR'] + filename)
                new_debt.photo = filename
            new_debt = Debt.create(new_debt)
            session['newest_id'] = new_debt.debt_id
            flash("Form all good.")
            return redirect(url_for('main.index'))


@debt.route('/id/<int:debt_id>')
def show_debt(debt_id):
    data = Debt.get(debt_id=debt_id)
    # form = AddNewDebtForm(obj=data)
    return render_template('detail.html', data=data)


@debt.route('/id/<int:debt_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_debt(debt_id):
    data = Debt.get(debt_id=debt_id)
    form = AddNewDebtForm(obj=data)
    if request.method == 'GET':
        return render_template('edit.html', form=form, debt_id=debt_id)
    if request.method == 'POST':
        if not form.validate():
            flash("Form didn't validate")
            return render_template('edit.html', form=form)
        else:
            form.photo.data = data.photo
            form.populate_obj(data)
            db.session.commit()
            flash('Form all good.')
            return redirect(url_for('.show_debt', debt_id=debt_id))


# @debt.route('/debts/id/<int:debt_id>', methods=['DELETE'])
@debt.route('/id/<int:debt_id>/delete')
@login_required
def delete_debt(debt_id):
    Debt.delete(debt_id)
    flash('Debt with id={} has been deleted'.format(debt_id))
    return redirect(url_for('main.index'))
