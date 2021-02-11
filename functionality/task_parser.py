"""
Extract the task data from user input.
"""


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
        return self._task_str.split(";")[0].lower()

    @property
    def name(self):
        """
        Return the name of the task.
        """
        return self._task_str.split(";")[1]

    def validate(self):
        """
        Validate the task string. Raise TaskFromatError on invalid format.

        Only checks that the task contains at least two parts separated with a
        semicolon.
        """
        if len(self._task_str.split(";")) < 2:
            raise TaskFormatError("Task string {} does not seem to contain "
                                  "a valid task with task type and task name "
                                  "in it, separated by a semicolon (;).")


class TaskFormatError(ValueError):
    """
    Error for signaling that faulty task format was encountered
    """
