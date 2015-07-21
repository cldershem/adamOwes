#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.controller.py
~~~~~~~~~~~~~~~~~

Main routes for application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/$SOME_REPO
"""
from flask import render_template, request, flash, current_app
from app import db
from app.models import Debt  # , Photo
from app.forms import AddNewDebtForm
from . import main
from datetime import datetime
from werkzeug import secure_filename


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = AddNewDebtForm()

    data = {
        "all": Debt.query.all(),
        "moneyLoaned": Debt.query.filter_by(debt_type="money"),
        "itemLoaned": Debt.query.filter_by(debt_type="item"),
        "itemStored": Debt.query.filter_by(debt_type="storage"),
        "promisesMade": Debt.query.filter_by(debt_type="promise"),
        "totals": {},
        "people": db.session.query(Debt.to_whom.distinct())
    }

    def get_interest(debt):
        return debt.interest

    def get_fees(debt):
        return debt.fees

    def get_oldeest_debt(person):
        debts = Debt.query.filter_by(to_whom=person).order_by(Debt.debt_date)
        date = debts[0].debt_date
        return datetime.utcnow() - date

    def get_person_totals(list_of_people):
        list_of_people = [r[0] for r in list_of_people]
        list_of_totals = []

        for person in list_of_people:
            total = 0
            oldest_debt = get_oldeest_debt(person)
            debts = Debt.query.filter_by(to_whom=person).all()
            # debts = [x.amount for x in debts]
            for debt in debts:
                total += debt.amount
                total += get_interest(debt)
                total += get_fees(debt)
            list_of_totals.append((person, total, oldest_debt))

        return list_of_totals

    data['totals']['people'] = get_person_totals(data['people'])
    data['totals']['everyone'] = sum([x[1] for x in data['totals']['people']])
    num_of_people = len(data['totals']['people'])
    if num_of_people > 0:
        data['totals']['per_person'] = \
            (data['totals']['everyone'] / num_of_people)
    data['upload_dir'] = current_app.config['UPLOAD_DIR']

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
                )
            if form.interest.data:
                new_debt.interest = form.interest.data
            if form.fees.data:
                new_debt.fees = form.fees.data
            if form.photo.data:
                filename = secure_filename(form.photo.data.filename)
                form.photo.data.save(data['upload_dir'] + filename)
                new_debt.photo = filename
            db.session.add(new_debt)
            db.session.commit()
            data['newest_id'] = new_debt.debt_id
            flash("Form all good.")
            return render_template('index.html', form=form, data=data)
