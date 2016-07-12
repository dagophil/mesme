import logging

from .database_connector import DatabaseConnector
from .database_types import User, Task, TrackEntry


TASK_WORK = 0
GENERAL_WORK = 1


class UserManagement(object):

    def __init__(self, user_name, database_location):
        self._user = User(name=user_name)
        self._database = DatabaseConnector(database_location)
        self._database.create_user(self._user)
        self.open_tasks = self._database.get_open_tasks(self._user.uid)

    def create_task(self, title, description):
        task = Task(user_uid=self._user.uid, title=title, description=description, type_id=TASK_WORK)
        self._database.create_task(task)
        return task.uid

    def delete_task(self, task_uid):
        task = Task(uid=task_uid, deleted=True)
        self._database.update_task(task)

    def task_done(self, task_uid):
        task = Task(uid=task_uid, done=True)
        self._database.update_task(task)

    def start_track_entry(self, task_uid):
        now = self._database.get_current_timestamp()
        entry = TrackEntry(task_uid=task_uid, timestamp_begin=now)
        self._database.create_track_entry(entry)
        return entry.uid

    def stop_track_entry(self, track_entry_uid):
        now = self._database.get_current_timestamp()
        entry = TrackEntry(uid=track_entry_uid, timestamp_end=now)
        self._database.update_track_entry(entry)
