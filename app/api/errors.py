#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api.errors
~~~~~~~~~~~~~~~~~

Default errors for api.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/$SOME_REPO
"""
from . import api


class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, data=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        # if data is not None:
        self.data = data
        self.response = api.Response(
            success=False,
            data=data,
            message=message,
            )


@api.errorhandler(APIError)
def handle_invalid_usage(error):
    return error.response.to_json()
