import os
import warnings

class FlaskConfig():
    """
    Configuration class for the Flask app.

    Environment variables are preferred, but if not available, a hard-coded
    value is used instead.
    """
    if os.environ.get("SECRET_KEY"):
        SECRET_KEY = os.environ.get("SECRET_KEY")
    else:
        warnings.warn("SECRET_KEY not set: insecure key used", RuntimeWarning)
        SECRET_KEY = "hardcoded-key-just-for-development-use"
