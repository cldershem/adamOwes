#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.controller.py
~~~~~~~~~~~~~~~~~

Main routes for application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import (render_template, request, flash, current_app, redirect,
                   url_for, session)
from app import db
from app.models import Debt  # , Photo
from app.main.forms import AddNewDebtForm
from . import main
from werkzeug import secure_filename


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = AddNewDebtForm()
    data = Debt.get_totals()

    if request.method == 'GET':
        if 'newest_id' in session:
            data['newest_id'] = session['newest_id']
            # session.pop('newest_id')
        return render_template('index.html', form=form, data=data)
    if request.method == 'POST':
        if not form.validate():
            flash("Form didn't validate.")
            return render_template('index.html', form=form, data=data)
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
            return redirect(url_for('.index'))


@main.route('/debts')
def list_debts():
    data = Debt.get()
    return render_template('list.html', data=data)


@main.route('/debts/id/<int:debt_id>')
def show_debt(debt_id):
    data = Debt.get_by_id(debt_id=debt_id)
    # form = AddNewDebtForm(obj=data)
    return render_template('detail.html', data=data)


@main.route('/debts/id/<int:debt_id>/edit', methods=['GET', 'POST'])
def edit_debt(debt_id):
    data = Debt.get_by_id(debt_id=debt_id)
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


# @main.route('/debts/id/<int:debt_id>', methods=['DELETE'])
@main.route('/debts/id/<int:debt_id>/delete')
def delete_debt(debt_id):
    Debt.delete(debt_id)
    flash('Debt with id={} has been deleted'.format(debt_id))
    return redirect(url_for('.index'))
