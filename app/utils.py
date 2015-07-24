#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.utils
~~~~~~~~~~~~~~~~~

Misc utilities for use throughout the application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""


def format_datetime(date, dt_format='%Y-%m-%d'):
    return date.strftime(dt_format)
