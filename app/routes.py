"""
Routes for the web app
"""

from flask import render_template, flash
import time

from app import app
from app.forms import ChallengeForm


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The index page: this will offer the challenge creation form.
    """
    challenge_form = ChallengeForm()
    if challenge_form.validate_on_submit():
        flash("Got challenge creation request from {}"
              "".format(challenge_form.habitica_id.data))
        time.sleep(4)
    return render_template("index.html", form=challenge_form)
