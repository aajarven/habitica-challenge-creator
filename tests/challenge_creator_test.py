"""
Unit tests for ChallengeCreator
"""

import pytest

from challenge_creator.challenge_creator import ChallengeCreator


@pytest.fixture
def valid_challenge_string():
    """
    Return a challenge string
    """
    return ("Test challenge name\n"
            "test short name\n"
            "Summary here\n"
            "And description here\n"
            "00000000-0000-4000-A000-000000000000\n"
            "Getting Organized;Creativity\n"
            "123\n"
            "Tasks\n"
            "Daily;Daily 1;An easy everyday task;Easy;1/1/2021;Weekly;1;"
            "SMTWHFA\n"
            "Habit;Habit 1;A medium habit;Medium;2/12/2021\n"
            "Daily;Daily 2;A hard daily for weekdays;Hard;1/1/2021;Weekly;1;"
            "MTWHF\n"
            "Habit;To-Do 1;A hard todo, due by the end of February;Hard;"
            "2/28/2021\n"
            "Daily;To-Do 2;An easy daily to be done on the 15th of February;"
            "Easy;2/15/2021;Weekly;1;0\n"
            "Habit;Habit 2;A medium habit starting on February 1st;Medium;"
            "2/1/2021\n"
            "End Tasks"
            )


# pylint: disable=redefined-outer-name
def test_name(valid_challenge_string):
    """
    Test that the challenge name is parsed correctly from the data.
    """
    creator = ChallengeCreator(valid_challenge_string)
    assert creator.name == "Test challenge name"


def test_short_name(valid_challenge_string):
    """
    Test that the challenge shortname is parsed correctly from the data.
    """
    creator = ChallengeCreator(valid_challenge_string)
    assert creator.short_name == "test short name"


def test_summary(valid_challenge_string):
    """
    Test that the challenge summary is parsed correctly from the data.
    """
    creator = ChallengeCreator(valid_challenge_string)
    assert creator.summary == "Summary here"


def test_description(valid_challenge_string):
    """
    Test that the challenge description is parsed correctly from the data.
    """
    creator = ChallengeCreator(valid_challenge_string)
    assert creator.description == "And description here"


def test_guild(valid_challenge_string):
    """
    Test that guild is parsed correctly from the data.
    """
    creator = ChallengeCreator(valid_challenge_string)
    assert creator.guild == "00000000-0000-4000-A000-000000000000"
