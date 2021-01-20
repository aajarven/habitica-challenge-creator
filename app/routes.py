"""
Routes for the web app
"""

from flask import render_template
from app import app
from app.forms import ChallengeForm


@app.route("/")
@app.route("/index")
def index():
    """
    The index page: this will offer the challenge creation form.
    """
    challenge_form = ChallengeForm()
    return render_template("index.html", form=challenge_form)
