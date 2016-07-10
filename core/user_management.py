import logging

from .database_connector import DatabaseConnector
from .database_types import User, Task


TASK_WORK = 0
GENERAL_WORK = 1


class UserManagement(object):

    def __init__(self, user_name, database_location):
        self._user = User(name=user_name)
        self._database = DatabaseConnector(database_location)
        self._database.create_user(self._user)
        self.open_tasks = self._database.get_open_tasks(self._user.uid)

    def create_task(self, title, description):
        """
        Create a task with the given title and description. Returns the task uid.
        :param title: The title.
        :param description: The description.
        :return: The task uid.
        """
        task = Task(user_uid=self._user.uid, title=title, description=description, type_id=TASK_WORK)
        self._database.create_task(task)
        return task.uid

    def delete_task(self, task_uid):
        """
        Delete the task with the given uid.
        :param task_uid: The task uid.
        """
        task = Task(uid=task_uid, deleted=True)
        self._database.update_task(task)

    def task_done(self, task_uid):
        """
        Set the task with the given uid to done.
        :param task_uid: The task uid.
        """
        task = Task(uid=task_uid, done=True)
        self._database.update_task(task)
