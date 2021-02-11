"""
Tests for task parsing classes.
"""

import pytest

from functionality.task_parser import (
        TaskParser, DifficultyParser, HabitParser, TaskFormatError,
        TaskTypeError)


@pytest.mark.parametrize(
        ["task_type", "task_name", "notes"],
        [
            ("daily", "test", "note"),
            ("todo", "todoname", "another note"),
            ("habit", "habitname", "note"),
            ("reward", "rewardname", "long note here: lot of stuff"),
            ("daily", "test longer name", "note here"),
            ("daily", "test dïfficúlt näme", "härd nötes äre härd"),
        ])
def test_simple_task(task_type, task_name, notes):
    """
    Test TaskParser with the simplest possible task.

    Ensure that task_type and name are determined as they should be according
    to the only currently allowed task syntax pattern.
    """
    parser = TaskParser("{};{};{}".format(task_type, task_name, notes))
    assert parser.task_type == task_type.lower()
    assert parser.name == task_name
    assert parser.notes == notes


def test_task_type_whitespace_strip():
    """
    Ensure that whitespace around task type is ignored
    """
    parser = TaskParser(" habit    ;that needs whitespace strip;note")
    assert parser.task_type == "habit"


def test_task_name_whitespace_strip():
    """
    Ensure that whitespace around task name is ignored
    """
    parser = TaskParser("habit; that needs whitespace strip ;notes")
    assert parser.name == "that needs whitespace strip"


def test_case_insensitive_task_type():
    """
    Ensure that task type is not case sensitive but is converted to lowercase
    """
    parser = TaskParser("HABIT;test case-insensitive type;note")
    assert parser.task_type == "habit"


def test_invalid_task():
    """
    Ensure that a TaskFormatError is raised when an invalid task is given.
    """
    with pytest.raises(TaskFormatError):
        TaskParser("daily that doesn't have a semicolon separating the type "
                   "and name")


@pytest.mark.parametrize(
        ["difficulty_input", "expected_difficulty"],
        [
            ("trivial", "trivial"),
            ("easy", "easy"),
            ("medium", "medium"),
            ("hard", "hard"),
            ("TRIVIAL", "trivial"),
            ("  easy    ", "easy"),
        ])
def test_difficulty_parser(difficulty_input, expected_difficulty):
    """
    Test task difficulty parsing.
    """
    parser = DifficultyParser("type;title;notes;{}".format(difficulty_input))
    assert parser.difficulty == expected_difficulty


def test_missing_difficulty():
    """
    Ensure that a TaskFormatError is raised when difficulty is not given
    """
    with pytest.raises(TaskFormatError) as err:
        DifficultyParser("type;title; no difficulty here =(")
    assert "at least four attributes" in str(err.value)


def test_unexpected_difficulty():
    """
    Ensure that a TaskFormatError is raised for an invalid difficulty
    """
    with pytest.raises(TaskFormatError) as err:
        DifficultyParser("type;title;notes;impossible")
    assert "Unexpected task difficulty 'impossible'" in str(err.value)


def test_habit_parser():
    """
    Parse a habit using HabitParser
    """
    parser = HabitParser("habit;test habit;a note here;easy")
    assert parser.task_type == "habit"
    assert parser.name == "test habit"
    assert parser.notes == "a note here"
    assert parser.difficulty == "easy"


def test_habit_parser_type_validation():
    """
    Ensure that a TaskTypeError raises when a non-habit is HabitParsed.
    """
    with pytest.raises(TaskTypeError) as err:
        HabitParser("todo;wrong type habit; note; hard")
    assert "task with type 'todo' using a parser for habits" in str(err.value)
