"""This is the main file for our Bookmark App."""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
bookmarks = []
app.config['SECRET_KEY'] = '9\xbcl\xeb\x83s\xa5]\xf7 +5c\xbd\xafh)\xfcts\xb2Y\x1f\xbd'

def store_bookmark(url):
    """Function that stores the bookmarks as dicts in a list."""
    bookmarks.append(dict(
        url = url,
        user = "reindert",
        date = datetime.utcnow
    ))

@app.route('/')
@app.route('/index')
def index():
    """View Function that is returned as a Response for a HTTP Request."""
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    """View Function for adding a Bookmark."""
    if request.method == "POST":
        url = request.form['url']
        store_bookmark(url)
        flash("Stored Bookmark '{}'".format(url))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.errorhandler(404)
def page_not_found(e):
    """View Function that returns the 404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """View Function that returns the 500 error page."""
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
