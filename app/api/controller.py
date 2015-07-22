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
        error="API docs not yet implemented"
        )
    return result.to_json(), 501


@mod.route('/debts/type/<string:debt_type>', defaults={'details': False})
@mod.route('/debts/type/<string:debt_type>/details',
           defaults={'details': True})
def get_by_type(debt_type, details):
    if details:
        data = {'debt_ids': Debt.get_by_type(debt_type, id_only=False)}
        message = "ids url = /debts/type/<debt_type>"
    else:
        data = {'debt_ids': Debt.get_by_type(debt_type, id_only=True)}
        message = "details url = /debts/type/<debt_type>/details"
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids']),
        message=message,
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


@mod.route('/debts', defaults={'details': False})
@mod.route('/debts/details', defaults={'details': True})
def get_debts(details):
    if details:
        data = {'debt_ids': Debt.get_list(id_only=False)}
        message = "ids url = /debts"
    else:
        data = {'debt_ids': Debt.get_list(id_only=True)}
        message = "details url = /debts/details"
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids']),
        message=message
        )
    return result.to_json(), 200
