"""
Routes for the web app
"""

from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
def index():
    """
    The index page: this will offer the challenge creation form.
    """
    return render_template("index.html")
