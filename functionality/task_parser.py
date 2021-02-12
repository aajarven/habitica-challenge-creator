"""
Extract the task data from user input.
"""

import datetime
import re


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

    def _parse_date(self, date_str, field):  # pylint: disable=no-self-use
        """
        Return a Date corresponding to the given string.

        Given in format DD.MM.YYYY. Raises a TaskFormatError with a descriptive
        error message if date cannot be parsed.

        :date_str: string in dd.mm.yyyy format
        :field: name of the property for which the date is parsed, used in the
                error message
        """
        try:
            return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError as err:
            raise (
                TaskFormatError("Unexpected {} value '{}' encountered. "
                                "Dates must be given in format 'DD.MM.YYYY'."
                                "".format(field, date_str))
                ) from err


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
        return self._parse_date(date_str, "due date")

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


class DailyParser(DifficultyParser):
    """
    A parser for dailies
    """

    @property
    def start_date(self):
        """
        Start date for the task as a Date object.

        Given in format DD.MM.YYYY.
        """
        date_str = self._task_str.split(";")[4].strip()
        return self._parse_date(date_str, "start date")

    @property
    def frequency(self):
        """
        Frequency of the daily.

        Allowed values are "daily", "weekly", "monthly" and "yearly".
        """
        return self._task_str.split(";")[5].strip().lower()

    @property
    def every_x(self):
        """
        Number of days between occurrences for a daily.

        Values other than 1 are only allowed when frequency is set to "daily".
        """
        every_x_str = self._task_str.split(";")[6].strip()
        try:
            return int(every_x_str)
        except ValueError as err:
            raise TaskFormatError("Illegal every_x value \"{}\" encountered: "
                                  "the value must be an integer."
                                  "".format(every_x_str)) from err

    @property
    def repeat(self):
        """
        Reads a lits of weekday letters and returns a weekday dict for the API.

        Days of the week in the input are depicted as follows:
          - M = Monday
          - T = Tuesday
          - W = Wednesday
          - H = Thursday
          - F = Friday
          - A = Saturday
          - S = Sunday
        And for the output the day abbreviations are "m", "t", "w", "th", "f",
        "s" and "su". The abbreviations are used as keys in the returned dict,
        with their boolean values representing whether the daily should occur
        on that day.

        Only has an effect when frequency is set to "weekly".
        """
        day_str = self._repeat_str()
        return {
                "m": "M" in day_str,
                "t": "T" in day_str,
                "w": "W" in day_str,
                "th": "H" in day_str,
                "f": "F" in day_str,
                "s": "A" in day_str,
                "su": "S" in day_str,
                }

    def _repeat_str(self):
        """
        Return the string from which `repeat` should be parsed from.
        """
        return self._task_str.split(";")[7].strip().upper()

    def validate(self):
        """
        In addition to all checks done by DifficultyParser, checks that:
        - task type is "daily"
        - task string has 8 fields separated with a semicolon
        - task has a valid start date
        - `frequency` is one of the allowed values
        - `every_x` is a positive integer
        - if `frequency` is not "daily", `every_x` is 1
        - all letters in `repeat` are legal weekday markers
        """
        super().validate()
        if self.task_type != "daily":
            raise TaskTypeError("Attempted to parse a task with type "
                                "'{}' using a parser for dailies."
                                "".format(self.task_type))
        if len(self._task_str.split(";")) != 8:
            raise TaskFormatError("Task string '{}' does not seem to "
                                  "contain a valid daily: they must "
                                  "have eight attributes (type, "
                                  "title, notes, difficulty, start date, "
                                  "frequency, every_x and repeat) "
                                  "separated by a semicolon (;)"
                                  "".format(self._task_str))
        self.start_date  # pylint: disable=pointless-statement
        if self.frequency not in ["daily", "weekly", "monthly", "yearly"]:
            raise TaskFormatError("Illegal frequency value \"{}\" "
                                  "encountered. Allowed values are \"daily\", "
                                  "\"weekly\", \"monthly\" and \"yearly\"."
                                  "".format(self.frequency))
        if self.every_x < 1:
            raise TaskFormatError("Value of every_x cannot be zero or "
                                  "negative.")
        if self.frequency != "daily" and self.every_x != 1:
            raise TaskFormatError("every_x can be set to a value other than 1 "
                                  "only when frequency is \"daily\".")
        if not re.match(r"\b(?!(?:.\B)*(.)(?:\B.)*\1)[MTWHFSA]+\b",
                        self._repeat_str()):
            raise TaskFormatError("Illegal weekday marker found in repeat "
                                  "value {}. Legal weekday markers are M, T, "
                                  "W, H, F, A and S."
                                  "".format(self._repeat_str()))


class TaskFormatError(ValueError):
    """
    Error for signaling that faulty task format was encountered
    """


class TaskTypeError(TypeError):
    """
    Error for signaling that a wrong type of task was given to a parser.
    """
