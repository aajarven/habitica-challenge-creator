from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, UUID


class ChallengeForm(FlaskForm):
    """
    A form for submitting challenge information.
    """
    habitica_id = StringField("Habitica user ID", validators=[
        UUID("This does not look like a valid Habitica user ID"),
        ])
    create_challenge = SubmitField("Create a new challenge")
