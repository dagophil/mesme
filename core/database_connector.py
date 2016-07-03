import logging
import datetime
import json
import sqlite3

from .database_types import User, Setting, Task, TrackEntry
from .database_types import create_table, insert_object, update_object


class DatabaseConnector(object):
    """
    The DatabaseConnector connects to a database and wraps the database queries.
    """

    def __init__(self, database_location):
        """
        Creates the database file and the necessary tables. If the database file already exists, it will not be
        overwritten.
        :param database_location: Path to the database.
        """
        self._date_format = "%Y-%m-%dT%H:%M:%S:%f"
        self._connection = sqlite3.connect(database_location)
        c = self._connection.cursor()
        tables = {
            "Users": User,
            "Settings": Setting,
            "Tasks": Task,
            "TrackEntries": TrackEntry
        }
        for table_name, object_class in tables.items():
            create_table(self._connection, table_name, object_class, if_not_exists=True)

    def __del__(self):
        """
        Closes the database connection.
        :return:
        """
        self.close()

    def close(self):
        """
        Closes the database connection.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @property
    def date_format(self):
        """
        Returns the date format.
        :return: The date format.
        """
        return self._date_format

    def create_user(self, user):
        """
        Inserts the user into the database and sets user.uid to the user uid.
        If the user already exists in the database, it is not inserted a second time and user.uid is set to the uid of
        the existing entry.
        :param user: The user object.
        """
        assert isinstance(user, User)
        try:
            existing_user = self.get_user(user.name)
            user.uid = existing_user.uid
        except KeyError:
            insert_object(self._connection, "Users", user)

    def get_user(self, name):
        """
        Returns the user with the given name. Raises a KeyError if the given name is not found in the database.
        :param name: The name.
        :return: The user.
        """
        assert isinstance(name, str)
        c = self._connection.cursor()
        c.execute("SELECT * FROM `Users` WHERE `name`=?;", (name,))
        row = c.fetchone()
        if row is None:
            raise KeyError("No user found with the name %s." % name)
        else:
            return User(*row)

    def update_user(self, user):
        """
        Use all not-None values from the given user and use them to overwrite the respective fields of the user with the
        given uid.
        :param user: The user database object.
        """
        assert isinstance(user, User)
        update_object(self._connection, "Users", user, ignore_none=True)

    def create_setting(self, setting):
        """
        Inserts the setting into the database and sets setting.uid and setting.timestamp_create.
        Raises a TypeError if the setting value cannot be converted to JSON via json.dumps.
        :param setting: The setting.
        """
        assert isinstance(setting, Setting)

        # Temporarily overwrite the value with its json string.
        old_value = setting.value
        setting.value = json.dumps(setting.value)

        # Set the timestamp and insert the setting into the database.
        setting.timestamp_create = self.get_current_timestamp()
        insert_object(self._connection, "Settings", setting)

        # Replace the json string with the actual value.
        setting.value = old_value

    def get_setting(self, user_uid, key):
        """
        Returns the setting for the given user. Raises a KeyError if no setting is found that matches user and key.
        :param user_uid: The user uid.
        :param key: The setting key.
        :return: The setting.
        """
        assert isinstance(user_uid, int)
        assert isinstance(key, str)
        c = self._connection.cursor()
        c.execute("SELECT * FROM `Settings` WHERE `user_uid`=? AND `key`=? "
                  "ORDER BY `timestamp_create` DESC, `uid` DESC;", (user_uid, key))
        row = c.fetchone()
        if row is None:
            raise KeyError("No setting found with user_uid=%s and key=%s." % (user_uid, key))
        else:
            setting = Setting(*row)
            setting.value = json.loads(setting.value)
            return setting

    def create_task(self, task):
        """
        Inserts a new task into the database and sets task.uid, task.timestamp_create, and task.timestamp_orderby.
        :param task: The task.
        """
        assert isinstance(task, Task)
        task.timestamp_create = self.get_current_timestamp()
        task.timestamp_orderby = task.timestamp_create
        insert_object(self._connection, "Tasks", task)

    def get_all_tasks(self, user_uid):
        """
        Collects all tasks for the given user and returns them sorted by timestamp_orderby in ascending order.
        :param user_uid: The user uid.
        :return: List with tasks.
        """
        assert isinstance(user_uid, int)
        c = self._connection.cursor()
        c.execute("SELECT * FROM `Tasks` WHERE `user_uid`=? ORDER BY `timestamp_orderby` ASC, `uid` ASC;", (user_uid,))
        rows = c.fetchall()
        tasks = [Task(*row) for row in rows]
        return tasks

    def get_open_tasks(self, user_uid):
        """
        Collects all tasks for the given user where timestamp_done is not set and returns them sorted by
        timestamp_orderby in ascending order.
        :param user_uid: The user uid.
        :return: List with open tasks.
        """
        assert isinstance(user_uid, int)
        c = self._connection.cursor()
        c.execute("SELECT * FROM `Tasks` WHERE `user_uid`=? AND (`timestamp_done` is null OR `timestamp_done`='') "
                  "ORDER BY `timestamp_orderby` ASC, `uid` ASC;", (user_uid,))
        rows = c.fetchall()
        tasks = [Task(*row) for row in rows]
        return tasks

    def update_task(self, task):
        """
        Use all not-None values from the given task and use them to overwrite the respective fields of the task with the
        given uid.
        :param task: The task with the update values.
        """
        assert isinstance(task, Task)
        update_object(self._connection, "Tasks", task, ignore_none=True)

    def create_track_entry(self, entry):
        """
        Inserts a new track entry into the database and sets entry.uid.
        :param entry: The track entry.
        """
        raise NotImplementedError()

    def get_track_entries_for_task(self, task_uid):
        """
        Returns all track entries for the given task sorted by timestamp in ascending order.
        :param task_uid: The task uid.
        :return: List with the track entries.
        """
        raise NotImplementedError()

    def get_current_timestamp(self):
        """
        Returns a well-formatted current timestamp.
        :return: The timestamp.
        """
        now = datetime.datetime.now()
        return now.strftime(self.date_format)
