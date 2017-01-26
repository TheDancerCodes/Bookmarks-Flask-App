"""This is the main file for our Bookmark App."""
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    """View Function that is returned as a Response for a HTTP Request."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
