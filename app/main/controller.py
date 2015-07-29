#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.controller.py
~~~~~~~~~~~~~~~~~

Main routes for application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask import (render_template, request, session)
from app.models import Debt
from . import main


@main.route('/')
@main.route('/index')
def index():
    data = Debt.get_totals()

    if request.method == 'GET':
        if 'newest_id' in session:
            data['newest_id'] = session['newest_id']
            # session.pop('newest_id')
        return render_template('index.html', data=data)
