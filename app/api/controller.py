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


@mod.route('/debts/type/<string:debt_type>')
def get_by_type(debt_type):
    data = {'debt_ids': Debt.get_by_type(debt_type)}
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids'])
        )
    return result.to_json(), 200


@mod.route('/debts/id/<int:debt_id>')
def get_by_id(debt_id):
    data = {'debt': Debt.get_by_id(debt_id)}
    result = Response(
        success=True,
        data=data,
        )
    return result.to_json(), 200


@mod.route('/debts')
def get_debts():
    data = {'debt_ids': Debt.get_list()}
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids'])
        )
    return result.to_json(), 200
