"""
Routes for the web app
"""

from flask import render_template, flash

from app import app
from app.forms import ChallengeForm
from functionality.challenge_creator import ChallengeCreator


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The index page: this will offer the challenge creation form.
    """
    challenge_form = ChallengeForm()
    challenge_dict = None
    if challenge_form.validate_on_submit():
        challenge_creator = ChallengeCreator(
                challenge_form.challenge_data.data)
        challenge_dict = challenge_creator.to_ordered_dict()
    return render_template("index.html", form=challenge_form,
                           challenge_dict=challenge_dict)
