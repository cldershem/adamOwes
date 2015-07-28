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
from flask import jsonify, request
from app.models import Debt
from . import api


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


@api.route('/')
def api_index():
    raise api.APIError('API docs, not yet implemented.', status_code=501)


@api.route('/debts/type/<string:debt_type>', defaults={'details': False})
@api.route('/debts/type/<string:debt_type>/details',
           defaults={'details': True})
def get_by_type(debt_type, details):
    if details:
        debts = [debt.serialize() for debt in Debt.get(debt_type=debt_type)]
        data = {'debt_ids': debts}
        message = "ids url = /debts/type/<debt_type>"
    else:
        debts = [debt.debt_id for debt in Debt.get(debt_type=debt_type)]
        data = {'debt_ids': debts}
        message = "details url = /debts/type/<debt_type>/details"
    result = Response(
        success=True,
        data=data,
        length=len(data['debt_ids']),
        message=message,
        )
    return result.to_json(), 200


@api.route('/debts/id/<int:debt_id>')
def get_by_id(debt_id):
    debt = Debt.get(debt_id=debt_id).serialize()
    data = {'debt': debt}
    result = Response(
        success=True,
        data=data,
        )
    return result.to_json(), 200


@api.route('/debts/id/<int:debt_id>', methods=['DELETE'])
def delete_debt(debt_id):
    raise api.APIError('You are unauthenticated', status_code=401)

    Debt.delete(debt_id)
    message = "debt_id={} deleted".format(debt_id)
    result = Response(
        success=True,
        message=message,
        )
    return result.to_json(), 200


@api.route('/debts/id/<int:debt_id>', methods=['PUT'])
def update_debt(debt_id):
    raise api.APIError('You are unauthenticated', status_code=401)

    data = request.get_json()
    updated_debt = Debt.update(debt_id, data)

    message = "debt_id={} updated".format(debt_id)
    result = Response(
        success=True,
        data={'debt': updated_debt},
        message=message,
        )
    return result.to_json(), 200


@api.route('/debts', defaults={'details': False})
@api.route('/debts/details', defaults={'details': True})
def get_debts(details):
    if details:
        debts = [debt.serialize() for debt in Debt.get()]
        data = {'debts': debts}
        length = len(data['debts'])
        message = "ids url = /debts"
    else:
        debts = [debt.debt_id for debt in Debt.get()]
        data = {'debt_ids': debts}
        message = "details url = /debts/details"
        length = len(data['debt_ids']),
    result = Response(
        success=True,
        data=data,
        length=length,
        message=message
        )
    return result.to_json(), 200
