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
# from decimal import Decimal

DATE_TIME_NOW = datetime.datetime.utcnow()


class Debt(db.Model):
    debt_id = db.Column(db.Integer, primary_key=True)
    debt_type = db.Column(db.String(20))
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))
    # photo = db.relationship('Photo')
    photo = db.Column(db.String(120))
    amount = db.Column(db.Float(20))
    interest = db.Column(db.Float(20))
    fees = db.Column(db.Float(20))
    to_whom = db.Column(db.String(30))
    debt_date = db.Column(db.DateTime())
    date_created = db.Column(db.DateTime, default=DATE_TIME_NOW)
    date_modified = db.Column(db.DateTime, onupdate=DATE_TIME_NOW)
    # _amount_with_interest = db.Column(db.Float())

    def __init__(self, debt_type, description, amount, to_whom, debt_date,
                 photo=None, interest=0, fees=0, title=None):
        self.debt_type = debt_type
        self.description = description
        self.amount = amount
        self.to_whom = to_whom
        self.debt_date = debt_date
        self.interest = interest
        self.fees = fees
        self.title = title
        self._amount_with_interest = 0

    def __repr__(self):
        return '<Debt debt_id={}, title={}>'.format(
            self.debt_id, self.title)

    @property
    def amount_with_interest(self):
        amount = self.get_amount_with_interest()
        self._amount_with_interest = amount
        return amount

    @amount_with_interest.setter
    def amount_with_interest(self):
        amount = self.get_amount_with_interest()
        self._amount_with_interest = amount

    def get_amount_with_interest(self):
        principal = self.amount
        if self.fees:
            principal += self.get_fees()

        rate = self.interest / 100
        age = self.get_debt_age() + 1
        compound = 12

        total = 0
        for year in range(0, age):
            total = round(principal * (
                (1.0 + (rate/compound)) ** (year * compound)), 2)
        return total

    def get_fees(self):
        return self.fees

    def get_debt_age(self):
        return relativedelta(DATE_TIME_NOW, self.debt_date).years

    @staticmethod
    def get_oldest_debt(person):
        debts = Debt.query.filter_by(to_whom=person).order_by(Debt.debt_date)
        return debts[0].get_debt_age()

    @staticmethod
    def get_totals():
        people = db.session.query(Debt.to_whom.distinct())
        data = {
            # "moneyLoaned": Debt.query.filter_by(debt_type="money"),
            # "itemLoaned": Debt.query.filter_by(debt_type="item"),
            # "itemStored": Debt.query.filter_by(debt_type="storage"),
            # "promisesMade": Debt.query.filter_by(debt_type="promise"),
            # "totals": {
            #     "people": Debt.get_person_totals(people),
            # }
            "moneyLoaned": Debt.get_by_type(debt_type="money", id_only=False),
            "itemLoaned": Debt.get_by_type(debt_type="item", id_only=False),
            "itemStored": Debt.get_by_type(debt_type="storage", id_only=False),
            "promisesMade": Debt.get_by_type(
                debt_type="promise", id_only=False),
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
            # debts = Debt.query.filter_by(to_whom=person).all()
            debts = Debt.get_by_person(person, id_only=False)
            for debt in debts:
                # total = debt.get_amount_with_interest()
                total = debt.amount_with_interest
            list_of_totals.append((person, total, oldest_debt))

        return list_of_totals

    @staticmethod
    def get_list(id_only=True):
        if id_only:
            return [debt.debt_id for debt in Debt.query.all()]
        else:
            return [Debt.serialize(debt) for debt in Debt.query.all()]

    @staticmethod
    def get_by_person(person, id_only=True):
        if id_only:
            return [Debt.serialize(debt) for debt in
                    Debt.query.filter_by(to_whom=person).all()]
        else:
            return [debt for debt in
                    Debt.query.filter_by(to_whom=person).all()]

    @staticmethod
    def get_by_type(debt_type, id_only=True):
        if id_only:
            return [debt.debt_id for debt in
                    Debt.query.filter_by(debt_type=debt_type).all()]
        else:
            return [Debt.serialize(debt) for debt in
                    Debt.query.filter_by(debt_type=debt_type).all()]

    @staticmethod
    def get_by_id(debt_id):
        debt = Debt.query.filter_by(debt_id=debt_id).first_or_404()
        return Debt.serialize(debt)

    @staticmethod
    def serialize(debt):
        debt_params = {
            'debt_id': debt.debt_id,
            'debt_type': debt.debt_type,
            'title': debt.title,
            'description': debt.description,
            'photo': debt.photo,
            'amount': debt.amount,
            'interest': debt.interest,
            'fees': debt.fees,
            'photo': debt.photo,
            'to_whom': debt.to_whom,
            'debt_date': debt.debt_date.strftime('%Y-%m-%d'),
            'date_created': debt.date_created.strftime('%Y-%m-%d'),
            'amount_with_interest': debt.amount_with_interest,
            }

        if debt.date_modified:
            debt_params['date_modified'] = debt.date_modified.strftime(
                '%Y-%m-%d')

        return debt_params


class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    # alt = db.Column(db.String(120))
    # title = db.Column(db.String(120))
    location = db.Column(db.String(200))
    debt_id = db.Column(db.Integer,
                        db.ForeignKey('debt.debt_id'))
    date_created = db.Column(db.DateTime, default=DATE_TIME_NOW)
    date_modified = db.Column(db.DateTime, onupdate=DATE_TIME_NOW)

    def __init__(self, location):
        # self.title = title
        # self.alt = alt
        self.location = location

    def __repr__(self):
        return '<Photo photo_id={}, title={}>'.format(
            self.photo_id, self.title)
