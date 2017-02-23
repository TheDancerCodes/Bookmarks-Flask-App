from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from thermos import db

# tags = db.Table('bookmark_tag',
#      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
#      db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
# )

tags = db.Table('bookmark_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags,
                            backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def latest_bookmarks(num):
        """Functon that returns latest bookmarks sorted by date."""
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]

    def __repr__(self):
        """Method to enable clear printing & logging of values."""
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        """
        Property password not represented in the db.
        Raises AttributeError if you try to read.
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """
        Setter for the password attribute.
        Generates a hash and stores it in the password_hash field.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks a string against the generated hash"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        """Pass this method a username & it returns the corresponding user."""
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        """Method to enable clear printing & logging of values."""
        return "<User '{}'>".format(self.username)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name
