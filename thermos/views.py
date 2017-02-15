from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app, db, login_manager
from forms import BookmarkForm, LoginForm
from models import User, Bookmark

@login_manager.user_loader
def load_user(userid):
    """View Function to retreive a user object based on the ID."""
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    """View Function that is returned as a Response for a HTTP Request."""
    return render_template('index.html', new_bookmarks=Bookmark.latest_bookmarks(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """View Function for adding a Bookmark."""
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored Bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/user/<username>')
def user(username):
    """View Function displaying a users Bookmarks."""
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    """View Function that logs users in."""
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            flash("Logged in succesfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('index'))
        flash("Incorrect Username or Password.")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """View Function that logs out users and redirects them to index page."""
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """View Function that returns the 404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """View Function that returns the 500 error page."""
    return render_template('500.html'), 500
