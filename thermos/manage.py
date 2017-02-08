#! /usr/bin/env python

from thermos import app, db
from flask_script import Manager, prompt_bool

from thermos import db
from models import User

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="Taracha", email="rojtaracha@gmail.com"))
    db.session.add(User(username="Shem", email="shem@gmail.com"))
    db.session.commit()
    print 'Initialized the database.'

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
        db.drop_all()
        print 'Dropped the database.'

if __name__ == '__main__':
    manager.run()
