"""This is the main file for our Bookmark App."""
from flask import Flask, render_template, url_for

app = Flask(__name__)

class User:
    """A User Class."""

    def __init__(self, firstname, lastname):
        """Function that initializes the User Class."""
        self.firstname = firstname
        self.lastname =  lastname

    def initials(self):
        """Function that returns initials of fname and lname."""
        return "{}. {}.".format(self.firstname[0], self.lastname[0])

@app.route('/')
@app.route('/index')
def index():
    """View Function that is returned as a Response for a HTTP Request."""
    return render_template('index.html', title="Title passed from View to Template.",
                            text=["first", "second", "third"],
                            user=User("Roger", "Taracha"))

@app.route('/add')
def add():
    """View Function for adding a Bookmark."""
    return render_template('add.html')

if __name__ == "__main__":
    app.run()
