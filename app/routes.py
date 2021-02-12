"""
Routes for the web app
"""

from flask import render_template, flash
from requests.exceptions import HTTPError

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
        if challenge_form.create_challenge.data:
            flash("Creating a new challenge")
            try:
                challenge_creator.create_challenge(
                        _header(challenge_form.habitica_id.data,
                                challenge_form.habitica_api_key.data))
            except HTTPError as err:  # TODO make this better
                flash(err.response.request)
                flash(err.response.content)
                import traceback
                traceback.print_exc()
        if challenge_form.show_challenge.data:
            flash("Showing the challenge")
    return render_template("index.html", form=challenge_form,
                           challenge_dict=challenge_dict)


def _header(user_id, api_key):
    """
    Return a Habitica API header for this app.

    :user_id: Habitica user ID of the person making the request
    :api_key: Habitica API keey of the person making the request
    :returns: A dict of headers for Habitica API calls
    """
    return {
        "x-api-user": user_id,
        "x-api-key": api_key,
        "x-client": "f687a6c7-860a-4c7c-8a07-9d0dcbb7c831-challenge_creator",
        }
