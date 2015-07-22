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
from flask import render_template, request, flash, current_app
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
                to_whom=form.person_owed.data,
                debt_date=form.date.data,
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
