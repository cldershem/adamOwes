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
                   url_for)
from app import db
from app.models import Debt  # , Photo
from app.forms import AddNewDebtForm
from . import main
from werkzeug import secure_filename


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = AddNewDebtForm()
    data = Debt.get_totals()

    if request.method == 'GET':
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
            db.session.add(new_debt)
            db.session.commit()
            data['newest_id'] = new_debt.debt_id
            flash("Form all good.")
            return render_template('index.html', form=form, data=data)


@main.route('/debts')
def list_debts():
    data = Debt.get_list(id_only=False)
    return render_template('list.html', data=data)


@main.route('/debts/id/<int:debt_id>', defaults={'edit': False})
@main.route('/debts/id/<int:debt_id>/edit', defaults={'edit': True},
            methods=['GET', 'POST'])
def show_debt(debt_id, edit):
    data = Debt.query.filter_by(debt_id=debt_id).first_or_404()
    form = AddNewDebtForm(obj=data)
    if not edit:
        return render_template('detail.html', data=data)
    else:
        if request.method == 'GET':
            return render_template('edit.html', form=form)
        if request.method == 'POST':
            if not form.validate():
                flash("Form didn't validate")
                return render_template('edit.html', form=form)
            else:
                form.photo.data = data.photo
                form.populate_obj(data)
                db.session.commit()
                flash('Form all good.')
                return redirect(url_for('.show_debt',
                                        debt_id=debt_id, edit=False))


@main.route('/debts/id/<int:debt_id>', methods=['DELETE'])
def delete_debt(debt_id):
    Debt.delete(debt_id)
    flash('Debt with id={} has been deleted'.format(debt_id))
    return redirect(url_for('.index'))
