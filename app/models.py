#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.models
~~~~~~~~~~~~~~~~~

DB models for application

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from app import db
import datetime
from dateutil.relativedelta import relativedelta


class Debt(db.Model):
    debt_id = db.Column(db.Integer, primary_key=True)
    debt_type = db.Column(db.String(20))
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))
    photo = db.Column(db.String(120))
    amount = db.Column(db.Float(20))
    interest = db.Column(db.Float(20))
    fees = db.Column(db.Float(20))
    to_whom = db.Column(db.String(30))
    debt_date = db.Column(db.DateTime())
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    compound_frequency = db.Column(db.String(20))
    is_active = db.Column(db.Boolean())

    compound_frequency_to_int = {
        'daily': 365,
        'weekly': 52,
        'monthly': 12,
        'quarterly': 4,
        'biannually': 2,
        'annually': 1,
        }

    def __init__(self, debt_type, description, amount, to_whom, debt_date,
                 photo=None, interest=0, fees=0, title=None,
                 compound_frequency='annually'):
        self.debt_type = debt_type
        self.description = description
        self.amount = amount
        self.to_whom = to_whom
        self.debt_date = debt_date
        self.interest = interest
        self.fees = fees
        self.title = title
        self.compound_frequency = compound_frequency
        self.is_active = True

    def __repr__(self):
        return '<Debt debt_id={}, title={}>'.format(
            self.debt_id, self.title)

    @property
    def amount_with_interest(self):
        principal = self.amount
        if self.fees:
            principal += self.get_fees()

        rate = self.interest / 100
        age = self.get_debt_age() + 1
        compound = Debt.compound_frequency_to_int[self.compound_frequency]

        total = 0
        for year in range(0, age):
            total = round(principal * (
                (1.0 + (rate/compound)) ** (year * compound)), 2)
        return total

    def get_fees(self):
        return self.fees

    def get_debt_age(self):
        return relativedelta(datetime.datetime.utcnow(), self.debt_date).years

    @staticmethod
    def get_oldest_debt(to_whom):
        debts = Debt.get(to_whom=to_whom)
        debts = sorted(debts, key=lambda debt: debt.debt_date)
        return debts[0].get_debt_age()

    @staticmethod
    def get_totals():
        people = db.session.query(
            Debt.to_whom.distinct()).filter_by(is_active=True)
        data = {
            "moneyLoaned": Debt.get(debt_type="money"),
            "itemLoaned": Debt.get(debt_type="item"),
            "itemStored": Debt.get(debt_type="storage"),
            "promisesMade": Debt.get(debt_type="promise"),
            "totals": {
                "people": Debt.get_person_totals(people),
            }
        }
        data['totals']['everyone'] = sum(
            [x[1] for x in data['totals']['people']])
        num_of_people = len(data['totals']['people'])
        if num_of_people > 0:
            data['totals']['per_person'] = \
                (data['totals']['everyone'] / num_of_people)

        return data

    @staticmethod
    def get_person_totals(list_of_people):
        list_of_people = [r[0] for r in list_of_people]
        list_of_totals = []

        for person in list_of_people:
            oldest_debt = Debt.get_oldest_debt(person)
            debts = Debt.get(to_whom=person)
            for debt in debts:
                total = debt.amount_with_interest
            list_of_totals.append((person, total, oldest_debt))

        return list_of_totals

    @staticmethod
    def get(**kwargs):
        """
        if no **kwargs, returns list of all active.
        """
        if kwargs:
            return [debt for debt in
                    Debt.query.filter_by(is_active=True,
                                         **kwargs).all()]
        else:
            return [debt for debt in
                    Debt.query.filter_by(is_active=True).all()]

    @staticmethod
    def get_by_id(debt_id):
        debt = Debt.query.filter_by(debt_id=debt_id).first_or_404()
        return debt

    def serialize(self):
        debt_params = {
            'debt_id': self.debt_id,
            'debt_type': self.debt_type,
            'title': self.title,
            'description': self.description,
            'photo': self.photo,
            'amount': self.amount,
            'interest': self.interest,
            'fees': self.fees,
            'photo': self.photo,
            'to_whom': self.to_whom,
            'debt_date': self.debt_date.strftime('%Y-%m-%d'),
            'date_created': self.date_created.strftime('%Y-%m-%d'),
            'amount_with_interest': self.amount_with_interest,
            'compound_frequency': self.compound_frequency,
            'is_active': self.is_active,
            }

        if self.date_modified:
            debt_params['date_modified'] = self.date_modified.strftime(
                '%Y-%m-%d')

        return debt_params

    @staticmethod
    def update(debt_id, data):
        debt = Debt.get(debt_id=debt_id)[0]
        # should probably validate data here

        for key, value in data.iteritems():
            setattr(debt, key, value)

        db.session.commit()
        new_debt = Debt.get_by_id(debt_id=debt_id)
        return Debt.serialize(new_debt)

    @staticmethod
    def delete(debt_id):
        debt = Debt.get(debt_id=debt_id)[0]
        debt.is_active = False
        db.session.commit()
        return True
