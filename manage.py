#! /usr/bin/env python

from thermos import app, db
from thermos.models import User, Bookmark
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

# Gives access to DB migration commands with a prefix of db
manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="Taracha", email="rojtaracha@gmail.com", password="test"))
    db.session.add(User(username="Shem", email="shem@gmail.com", password="test"))
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
