"""
Functionality for taking in user-supplied data and creating a challenge.
"""


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
