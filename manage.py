#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manage.py
~~~~~~~~~~~~~~~~~

Baremetal/maintenance for application.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/$SOME_REPM
"""
from app import create_app
from flask.ext.script import Manager


app = create_app('development')
manager = Manager(app)


@manager.command
@manager.option('--environment', 'e', help='development, production, test')
def run(environment='development'):
    """
    Runs application on localhost.
    """
    app = create_app(environment)
    app.run()


@manager.command
@manager.option('--environment', 'e', help='development, production, test')
def run_on_network(environment='development'):
    """
    Runs application on network making it accessable by other machines on
    the same network.
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
    Populates db with random dummy data.
    """
    from app.models import (Debt)
    from app import db
    import random
    from datetime import datetime
    import os

    dev_db = './tmp/dev.sqlite'

    if os.path.isfile(dev_db):
        os.rename(dev_db, dev_db + '.bak')

    db.create_all()

    list_o_types = ['money', 'item', 'storage', 'promise']
    list_o_people = ['Bob', 'Susan', 'Tom', 'Your Mom', 'Sally']
    list_o_descriptions = [
        'Something', 'Nothing', 'Noneya', 'Handy', 'Ice Cream']
    list_o_compounds = ['daily', 'weekly', 'monthly', 'biannually', 'annually']

    def get_random_date():
        year = random.randint(1980, 2015)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return ("{}-{}-{}".format(year, month, day))

    def populate_debt():
        for i in range(10):
            debt = Debt(
                debt_type=random.choice(list_o_types),
                description=random.choice(list_o_descriptions),
                to_whom=random.choice(list_o_people),
                amount=float(random.randrange(10000, 99999) / 100),
                fees=float(random.randrange(10000, 99999) / 100),
                interest=float(random.randrange(1000, 9999) / 100),
                debt_date=datetime.strptime(get_random_date(), '%Y-%m-%d'),
                compound_frequency=random.choice(list_o_compounds),
                )
            db.session.add(debt)
            db.session.commit()
            print("Created debt_id={}".format(debt.debt_type))

    populate_debt()


if __name__ == '__main__':
    manager.run()
