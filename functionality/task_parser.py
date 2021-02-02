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

    @property
    def task_type(self):
        """
        Return the task type.
        """
        return self._task_str.split(";")[0]
        # TODO: validation

    @property
    def name(self):
        """
        Return the name of the task.
        """
        return self._task_str.split(";")[1]
        # TODO: validation
