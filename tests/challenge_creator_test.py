"""
Unit tests for ChallengeCreator
"""

import pytest

from functionality.challenge_creator import ChallengeCreator


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


@pytest.fixture
def valid_challenge_dict():
    """
    Return the core data of the test challenge as a dict
    """
    return {
        "group": "00000000-0000-4000-A000-000000000000",
        "name": "Test challenge name",
        "shortName": "test short name",
        "summary": "Summary here",
        "description": "And description here",
        "prize": 123,
        }


@pytest.fixture
def header():
    return {"x-api-user": "fake-habitica-user-id",
            "x-api-key": "fake-habitica-api-key",
            "x-client": "fake-app-id"}


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


def test_prize(valid_challenge_string):
    """
    Test that guild is parsed correctly from the data.
    """
    creator = ChallengeCreator(valid_challenge_string)
    assert creator.prize == 123


def test_non_numeric_prize():
    """
    Test that a descriptive exception is raised for challenges with bad prize.
    """
    challenge = ("Test challenge name\n"
                 "test short name\n"
                 "Summary here\n"
                 "And description here\n"
                 "00000000-0000-4000-A000-000000000000\n"
                 "Creativity\n"
                 "three\n"  # non-numerical prize!
                 "Tasks\n"
                 "Daily;daily;-;Easy;1/1/2021;Weekly;1;SMTWHFA\n"
                 "End Tasks")
    creator = ChallengeCreator(challenge)
    with pytest.raises(ValueError) as err:
        prize = creator.prize  # noqa: F841 pylint: disable=unused-variable
    assert "Invalid gem prize value three encountered" in str(err.value)


def test_non_integer_prize():
    """
    Test that a decimal prize is not accepted
    """
    challenge = ("Test challenge name\n"
                 "test short name\n"
                 "Summary here\n"
                 "And description here\n"
                 "00000000-0000-4000-A000-000000000000\n"
                 "Creativity\n"
                 "1.2\n"  # non-integer prize!
                 "Tasks\n"
                 "Daily;daily;-;Easy;1/1/2021;Weekly;1;SMTWHFA\n"
                 "End Tasks")
    creator = ChallengeCreator(challenge)
    with pytest.raises(ValueError) as err:
        prize = creator.prize  # noqa: F841 pylint: disable=unused-variable
    assert "Invalid gem prize value 1.2 encountered" in str(err.value)


def test_challenge_creation(valid_challenge_string, valid_challenge_dict,
                            header, mocker):
    """
    Ensure that challenge creation posts the correct data to Habitica API
    """
    post_challenge = mocker.patch("habitica_helper.habrequest.post")
    mocker.patch("habitica_helper.habrequest.get")
    creator = ChallengeCreator(valid_challenge_string)
    creator.create_challenge(header)

    post_challenge.assert_called_once()
    post_challenge.assert_called_with("https://habitica.com/api/v3/challenges",
                                      data=valid_challenge_dict,
                                      headers=header)
