"""
Extract the task data from user input.
"""

import datetime


class TaskParser():
    """
    Base parser that can just parse task type and name of the task.
    """

    def __init__(self, task_str):
        """
        Create the parser.

        :task_str: String representing the task.
        """
        self._task_str = task_str
        self.validate()

    @property
    def task_type(self):
        """
        Return the task type.
        """
        return self._task_str.split(";")[0].lower().strip()

    @property
    def name(self):
        """
        Return the name of the task.
        """
        return self._task_str.split(";")[1].strip()

    @property
    def notes(self):
        """
        Return task notes.
        """
        return self._task_str.split(";")[2].strip()

    def validate(self):
        """
        Validate the task string. Raise TaskFromatError on invalid format.

        Only checks that the task contains at least two parts separated with a
        semicolon.
        """
        if len(self._task_str.split(";")) < 3:
            raise TaskFormatError("Task string {} does not seem to contain "
                                  "a valid task with task type, name and note"
                                  "in it, separated by a semicolon (;)."
                                  "".format(self._task_str))


class DifficultyParser(TaskParser):
    """
    Parser that is able to extract data for tasks with difficulty value.

    The format for a task is `type; title; notes; difficulty`.

    This parser is not supposed to be used as is, but to be subclassed instead.
    """

    @property
    def difficulty(self):
        """
        Return task difficulty.
        """
        return self._task_str.split(";")[3].lower().strip()

    def validate(self):
        """
        Validate the task string, raise TaskFormatError on invalid format.

        Check that:
         - there are four parts in the task string
         - the difficulty is one of the allowed values
        """
        super().validate()
        if len(self._task_str.split(";")) < 4:
            raise TaskFormatError("Task string '{}' does not seem to "
                                  "contain a valid {}: they must "
                                  "have at least four attributes (type, "
                                  "title, notes and difficulty) "
                                  "separated by a semicolon (;)"
                                  "".format(self._task_str, self.task_type))
        if self.difficulty not in ["trivial", "easy", "medium", "hard"]:
            raise TaskFormatError("Unexpected task difficulty '{}' "
                                  "encountered. Only values trivial, easy, "
                                  "medium and hard are allowed."
                                  "".format(self.difficulty))


class HabitParser(DifficultyParser):
    """
    A parser for habit type tasks.
    """

    def validate(self):
        """
        Validate the task string, raise TaskFormatError on invalid format.

        In addition to all checks done by DifficultyParser, checks that task
        type is "habit".
        """
        super().validate()
        if self.task_type != "habit":
            raise TaskTypeError("Attempted to parse a task with type "
                                "'{}' using a parser for habits."
                                "".format(self.task_type))


class TodoParser(DifficultyParser):
    """
    A parser for todo type tasks.
    """

    @property
    def date(self):
        """
        Due date for the task as a Date object.

        Given in format DD.MM.YYYY.
        """
        date_str = self._task_str.split(";")[4].strip()
        try:
            return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError as err:
            raise (
                TaskFormatError("Unexpected due date value '{}' encountered. "
                                "Dates must be given in format 'DD.MM.YYYY'."
                                "".format(date_str))
                ) from err

    def validate(self):
        """
        In addition to all checks done by DifficultyParser, checks that:
        - task type is "todo"
        - task has a valid due date
        """
        super().validate()
        if self.task_type != "todo":
            raise TaskTypeError("Attempted to parse a task with type "
                                "'{}' using a parser for todos."
                                "".format(self.task_type))
        if len(self._task_str.split(";")) != 5:
            raise TaskFormatError("Task string '{}' does not seem to "
                                  "contain a valid todo: they must "
                                  "have at least five attributes (type, "
                                  "title, notes, difficulty and due date) "
                                  "separated by a semicolon (;)"
                                  "".format(self._task_str))
        self.date  # pylint: disable=pointless-statement


class TaskFormatError(ValueError):
    """
    Error for signaling that faulty task format was encountered
    """


class TaskTypeError(TypeError):
    """
    Error for signaling that a wrong type of task was given to a parser.
    """
