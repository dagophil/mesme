import logging

from .database_connector import DatabaseConnector
from .database_types import User, Task, TrackEntry


TASK_WORK = 0
GENERAL_WORK = 1
PAUSE = 2


class UserManagement(object):

    def __init__(self, user_name, database_location):
        self._user = User(name=user_name)
        self._database = DatabaseConnector(database_location)
        self._database.create_user(self._user)
        self._current_task_uid = None

    @property
    def current_task_uid(self):
        return self._current_task_uid

    def get_open_tasks(self):
        tasks = self._database.get_open_tasks(self._user.uid)
        tasks = [task for task in tasks if task.type_id == TASK_WORK]
        return tasks

    def create_task(self, title, description):
        task = Task(user_uid=self._user.uid, title=title, description=description, type_id=TASK_WORK)
        self._database.create_task(task)
        return task.uid

    def create_general_work_task(self):
        task = Task(user_uid=self._user.uid, type_id=GENERAL_WORK)
        self._database.create_task(task)
        return task.uid

    def create_pause_task(self):
        task = Task(user_uid=self._user.uid, type_id=PAUSE)
        self._database.create_task(task)
        return task.uid

    def delete_task(self, task_uid):
        task = Task(uid=task_uid, deleted=True)
        self._database.update_task(task)

    def start_task(self, task_uid):
        self._current_task_uid = task_uid
        now = self._database.get_current_timestamp()
        entry = TrackEntry(task_uid=task_uid, timestamp_begin=now)
        self._database.create_track_entry(entry)
        return entry.uid

    def stop_current_task(self):
        if self._current_task_uid is not None:
            now = self._database.get_current_timestamp()
            entries = self._database.get_open_track_entries(self._current_task_uid)
            for entry in entries:
                entry.timestamp_end = now
                self._database.update_track_entry(entry)
            self._current_task_uid = None

    def task_done(self, task_uid):
        task = Task(uid=task_uid, done=True)
        self._database.update_task(task)
