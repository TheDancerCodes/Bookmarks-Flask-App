from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app, db, login_manager
from forms import BookmarkForm, LoginForm, SignupForm
from models import User, Bookmark, Tag

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
        tags = form.tags.data
        bm = Bookmark(user=current_user, url=url, description=description, tags=tags)
        db.session.add(bm)
        db.session.commit()
        flash("Stored Bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('bookmark_form.html', form=form, title="Add a Bookmark")

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    """View Function for editing a Bookmark."""
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}'".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title="Edit bookmark")

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
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in succesfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user',
                                                username=user.username))
        flash("Incorrect Username or Password.")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """View Function that logs out users and redirects them to index page."""
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please Login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    """View Function that returns the 404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """View Function that returns the 500 error page."""
    return render_template('500.html'), 500

@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)
