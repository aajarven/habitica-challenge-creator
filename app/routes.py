"""
Routes for the web app
"""

from app import app


@app.route("/")
@app.route("/index")
def index():
    """
    The index page: this will offer the challenge creation form.
    """
    return "<h1>Habitica Challenge Creator</h1>"
