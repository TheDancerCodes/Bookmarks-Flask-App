#! /usr/bin/env python

from thermos import app, db
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

# Gives access to DB migration commands with a prefix of db
manager.add_command('db', MigrateCommand)

@manager.command
def insert_data():
    """A utility function to insert test data into the database."""
    taracha = User(username="taracha", email="rojtaracha@gmail.com", password="test")
    db.session.add(taracha)


    def add_bookmark(url, description, tags):
        """Internal Function that adds new bookmarks."""
        db.session.add(Bookmark(url=url, description=description, user=taracha,
                                tags=tags))

    # loop that adds a list of tags.
    for name in ["dance", "choreography", "motion", "turnup", "hiphop", "kenya", "music", "dab", "hype", "afrobeat" ]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark("http://worldofdance.com/", "World Of Dance. [WOD]", "dance,choreography,motion,turnup")
    add_bookmark("http://www.hiphopinternational.com/", "HiphopInternational. [HHI]", "hiphop,kenya,music,dab,hype")
    add_bookmark("http://dance254.com/", "DANCE254. [KE]", "dance,motion,turnup,hiphop,kenya")

    shem = User(username="shem", email="shem@gmail.com", password="test")
    db.session.add(shem)
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
