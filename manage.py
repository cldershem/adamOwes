#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manage.py
~~~~~~~~~~~~~~~~~

Baremetal/maintence for application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/$SOME_REPM
"""
from app import create_app
from flask.ext.script import Manager


app = create_app('development')
manager = Manager(app)


@manager.command
def run():
    """
    """
    app = create_app('development')
    app.run()


@manager.command
def run_on_network():
    """
    """
    app = create_app('development')
    app.run('0.0.0.0')


@manager.command
def show_config():
    """
    Pretty prints current config.
    """
    from pprint import pprint

    print("Config:")
    pprint(dict(app.config))


@manager.command
def populate_db():
    """
    Populates db from yaml source.
    """
    # import yaml
    # from app.models import *
    from app import db
    # root = './tmp/data/'

    db.create_all()


if __name__ == '__main__':
    manager.run()
