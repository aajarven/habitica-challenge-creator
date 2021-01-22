from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, UUID
from wtforms.widgets import TextArea


class ChallengeForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """
    A form for submitting challenge information.
    """
    habitica_id = StringField("Habitica user ID", validators=[
        DataRequired("Field cannot be empty"),
        UUID("This does not look like a valid Habitica user ID"),
        ])
    habitica_api_key = StringField("Habitica API key", validators=[
        DataRequired("Field cannot be empty"),
        UUID("This does not look like a valid API key"),
        ])
    challenge_data = StringField(
            "Challenge data", widget=TextArea(),
            validators=[DataRequired("Field cannot be empty")],
            render_kw={"rows": 50, "cols": 120})
    create_challenge = SubmitField("Create a new challenge")
