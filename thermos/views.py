from flask import render_template, redirect, url_for, flash

from thermos import app, db
from forms import BookmarkForm
from models import User, Bookmark

# Fake Login [mocks the login process with a default user.]
def logged_in_user():
    return User.query.filter_by(username='Taracha').first()

@app.route('/')
@app.route('/index')
def index():
    """View Function that is returned as a Response for a HTTP Request."""
    return render_template('index.html', new_bookmarks=Bookmark.latest_bookmarks(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """View Function for adding a Bookmark."""
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored Bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    """View Function that returns the 404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """View Function that returns the 500 error page."""
    return render_template('500.html'), 500
