"""
Tests for task parsing classes.
"""

import pytest

from functionality.task_parser import TaskParser


@pytest.mark.parametrize(
        ["task_type", "task_name"],
        [
            ("daily", "test"),
            ("todo", "todoname"),
            ("habit", "habitname"),
            ("reward", "rewardname"),
            ("daily", "test longer name"),
            ("daily", "test dïfficúlt näme"),
        ])
def test_simple_task(task_type, task_name):
    """
    Test TaskParser with the simplest possible task.

    Ensure that task_type and name are determined as they should be according
    to the only currently allowed task syntax pattern.
    """
    parser = TaskParser("{};{}".format(task_type, task_name))
    assert parser.task_type == task_type
    assert parser.name == task_name
