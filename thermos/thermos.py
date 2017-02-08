"""This is the main file for our Bookmark App."""
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


# Determine path to current python file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '9\xbcl\xeb\x83s\xa5]\xf7 +5c\xbd\xafh)\xfcts\xb2Y\x1f\xbd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'birika.db')
# Initialise SQLAlchemy
# db variable reps DB connection & provides access to all flask_alchemy functionality
db = SQLAlchemy(app)

from forms import BookmarkForm
import models

# Fake Login [mocks the login process with a default user.]
def logged_in_user():
    return models.User.query.filter_by(username='Taracha').first()

@app.route('/')
@app.route('/index')
def index():
    """View Function that is returned as a Response for a HTTP Request."""
    return render_template('index.html', new_bookmarks=models.Bookmark.latest_bookmarks(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """View Function for adding a Bookmark."""
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored Bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    """View Function that returns the 404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """View Function that returns the 500 error page."""
    return render_template('500.html'), 500
