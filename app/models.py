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

    def __repr__(self):
        return '<Debt debt_id={}, title={}>'.format(
            self.debt_id, self.title)


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
