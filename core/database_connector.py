import logging
import datetime
import json
import sqlite3

from .database_types import User, Setting, Task, TrackEntry


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
        c.execute("CREATE TABLE IF NOT EXISTS `Users` ("
                  "`uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                  "`name` TEXT NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS `Settings` ("
                  "`uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                  "`user_uid` INTEGER NOT NULL, "
                  "`timestamp_create` TEXT NOT NULL, "
                  "`key` TEXT NOT NULL, "
                  "`value` TEXT NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS `Tasks` ("
                  "`uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                  "`user_uid` INTEGER NOT NULL, "
                  "`title` TEXT, "
                  "`description` TEXT, "
                  "`timestamp_create` TEXT NOT NULL, "
                  "`datetime_done` TEXT, "
                  "`timestamp_orderby` TEXT NOT NULL, "
                  "`type` INTEGER NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS `TrackEntries` ("
                  "`uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                  "`user_uid` INTEGER NOT NULL, "
                  "`task_uid` INTEGER, "
                  "`timestamp_begin` TEXT NOT NULL, "
                  "`timestamp_end` TEXT NOT NULL, "
                  "`description` TEXT, "
                  "`type` INTEGER NOT NULL);")
        self._connection.commit()

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
            user.uid = None
            c = self._connection.cursor()
            c.execute("INSERT INTO `Users` VALUES (?, ?);", user.field_values())
            self._connection.commit()
            uid = c.lastrowid
            user.uid = uid

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

    def create_setting(self, setting):
        """
        Inserts the setting into the database and sets setting.uid and setting.timestamp_create.
        Raises a TypeError if the setting value cannot be converted to JSON via json.dumps.
        :param setting: The setting.
        """
        assert isinstance(setting, Setting)
        setting.uid = None
        old_value = setting.value
        setting.value = json.dumps(setting.value)
        setting.timestamp_create = self._get_current_timestamp()
        c = self._connection.cursor()
        c.execute("INSERT INTO `Settings` VALUES (?, ?, ?, ?, ?);", setting.field_values())
        self._connection.commit()
        setting.uid = c.lastrowid
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
        task.uid = None
        task.timestamp_create = self._get_current_timestamp()
        task.timestamp_orderby = task.timestamp_create
        c = self._connection.cursor()
        c.execute("INSERT INTO `Tasks` VALUES (?, ?, ?, ?, ?, ?, ?, ?);", task.field_values())
        self._connection.commit()
        task.uid = c.lastrowid

    def get_all_tasks(self, user_uid):
        """
        Collects all tasks for the given user and returns them sorted by timestamp_orderby in ascending order.
        :param user_uid: The user uid.
        :return: List with tasks.
        """

    def get_open_tasks(self, user_uid):
        """
        Collects all tasks for the given user where timestamp_done is not set and returns them sorted by
        timestamp_orderby in ascending order.
        :param user_uid: The user uid.
        :return: List with open tasks.
        """
        raise NotImplementedError()

    def update_task(self, task_uid, task):
        """
        Use all not-None values from the given task and use them to overwrite the respective fields of the task with the
        given uid.
        :param task_uid: The task uid of the task that is updated.
        :param task: The task with the update values.
        """
        raise NotImplementedError()

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

    def _get_current_timestamp(self):
        """
        Returns a well-formatted current timestamp.
        :return: The timestamp.
        """
        now = datetime.datetime.now()
        return now.strftime(self.date_format)
