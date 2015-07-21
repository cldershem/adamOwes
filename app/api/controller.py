#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
api.controller.py
~~~~~~~~~~~~~~~~~

Controller for the api

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import Blueprint, jsonify
from app.models import Debt


mod = Blueprint('api', __name__, url_prefix='/api/v1')


def list_to_dict(list_to_convert):
    new_dict = dict(zip([x for x in range(0,
                        len(list_to_convert))], list_to_convert))
    return new_dict


class Response():
    """
    """
    def __init__(self, success=False, data=None, error=None,
                 page=None, **kwargs):
        self.success = success
        if error:
            self.error = error
        if data:
            self.data = data
        if page:
            self.page = page

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return jsonify(self.__dict__)

    def __repr__(self):
        return "<Response success={}, data={}, error={}>".format(
            self.success, self.data, self.error)


@mod.route('/')
def api():
    result = Response(
        success=False,
        error="API not yet implemented"
        )
    return result.to_json(), 501


@mod.route('/debts/<string:data_type>')
def get_by_type(data_type):
    list_of_debts = [debt.debt_id for debt in
                     Debt.query.filter_by(debt_type=data_type).all()]
    data = {'debt_ids': list_of_debts}
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids'])
        )
    return result.to_json(), 200


@mod.route('/debts')
def get_debts():
    list_of_debts = [debt.debt_id for debt in Debt.query.all()]
    data = {'debt_ids': list_of_debts}
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids'])
        )
    return result.to_json(), 200
