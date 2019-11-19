#! /usr/bin/env python

from my_app import app, db
from my_app.models import User, URL, Item
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="john", email="john@example.com", password="test"))
    db.session.add(User(username="doe", email="doe@example.com", password="test"))
    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool(
            "Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
