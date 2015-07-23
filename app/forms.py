#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.forms
~~~~~~~~~~~~~~~~~

Forms needed throughout app.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/adamOwes
"""
from flask_wtf import Form
from wtforms import (StringField, SelectField, SubmitField,
                     FileField, DecimalField, DateField)
from wtforms.validators import (DataRequired, )


class AddNewDebtForm(Form):
    """
    """
    form_id = 'addNewDebt'
    debt_type = SelectField('What type of debt?',
                            choices=[
                                ('money', 'Money Loaned'),
                                ('item', 'Item Loaned'),
                                ('storage', 'Item Stored'),
                                ('promise', 'Promises Made'),
                                ],
                            validators=[DataRequired()])
    description = StringField('Description',
                              validators=[DataRequired()],
                              description="120 characters max")
    photo = FileField('Photo')
    amount = DecimalField('Initial Amount', places=2, rounding=None,
                          validators=[DataRequired()], description="0.00")
    interest = StringField('Interest', description="0.00")
    fees = DecimalField('Fees', places=2, rounding=None, description="0.00")
    compound_frequency = SelectField('Compounds Per Year',
                                     choices=[
                                         ('daily', 'Daily'),
                                         ('weekly', 'Weekly'),
                                         ('monthly', 'Monthly'),
                                         ('quarterly', 'Quarterly'),
                                         ('biannually', 'BiAnnually'),
                                         ('annually', 'Annually'),
                                         ],
                                     default=1,
                                     validators=[DataRequired()])
    debt_date = DateField('Date', format='%Y-%m-%d',
                          description="YYYY-MM-DD")
    to_whom = StringField('To Whom',
                          validators=[DataRequired()],
                          description="John Smith")
    submit = SubmitField('Submit')
