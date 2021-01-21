"""
Functionality for taking in user-supplied data and creating a challenge.
"""

from habitica_helper.challenge import ChallengeTool


class ChallengeCreator():
    """
    Create Habitica challenges based on text data.

    The data is input in the format specified in
    https://github.com/Memry/Challenge-Creator
    """

    def __init__(self, data):
        """
        Create the class.

        :data: A string representation of the challenge. See
               https://github.com/Memry/Challenge-Creator.
        """
        self._raw_data = data
        self._rows = self._raw_data.split("\n")
        self._challenge = None

    def create_challenge(self, header):
        """
        Create a challenge from the data if not already created.

        A Challenge representing the challenge is returned to the caller.

        :header: Habitica API header dict
        :returns: The created Challenge
        """
        if not self._challenge:
            tool = ChallengeTool(header)
            challenge_data = {
                    "group": self.guild,
                    "name": self.name,
                    "shortName": self.short_name,
                    "summary": self.summary,
                    "description": self.description,
                    "prize": self.prize,
                    }
            self._challenge = tool.create_challenge(challenge_data)
        return self._challenge

    @property
    def name(self):
        """
        Return the name of the challenge in the string
        """
        return self._rows[0]

    @property
    def short_name(self):
        """
        Return the shortname for the challenge.
        """
        return self._rows[1]

    @property
    def summary(self):
        """
        Return the summary for the challenge.
        """
        return self._rows[2]

    @property
    def description(self):
        """
        Return the description for the challenge.
        """
        return self._rows[3]

    @property
    def guild(self):
        """
        Return the guild to which the challenge belongs.
        """
        return self._rows[4]

    @property
    def prize(self):
        """
        Return the size of the gem prize for the challenge winner.
        """
        try:
            return int(self._rows[6])
        except ValueError as err:
            raise ValueError("Invalid gem prize value {} encountered"
                             "".format(self._rows[6])) from err
