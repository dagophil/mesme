import logging
import datetime
import json
import sqlite3


class DatabaseConnector(object):

    def __init__(self, database_location):
        """
        Creates the database file and the necessary tables. If the database file already exists, it will not be
        overwritten.
        :param database_location: Path to the database.
        """
        self._date_format = "%Y-%m-%dT%H:%M:%S:%f"
        self._connection = sqlite3.connect(database_location)
        c = self._connection.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS `Users` (
                                       `uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                       `name` TEXT NOT NULL
                                   );""")
        c.execute("""CREATE TABLE IF NOT EXISTS "Settings" (
                                       `uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                       `user_uid` INTEGER NOT NULL,
                                       `timestamp_create` TEXT NOT NULL,
                                       `key` TEXT NOT NULL,
                                       `value` TEXT NOT NULL
                                   );""")
        c.execute("""CREATE TABLE IF NOT EXISTS "Tasks" (
                                       `uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                       `user_uid` INTEGER NOT NULL,
                                       `title` TEXT,
                                       `description` TEXT,
                                       `datetime_create` TEXT NOT NULL,
                                       `datetime_done` TEXT,
                                       `datetime_orderby` TEXT NOT NULL,
                                       `type` INTEGER NOT NULL
                                   );""")
        c.execute("""CREATE TABLE IF NOT EXISTS "TrackEntries" (
                                       `uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                       `user_uid` INTEGER NOT NULL,
                                       `task_uid` INTEGER,
                                       `datetime_begin` TEXT NOT NULL,
                                       `datetime_end` TEXT NOT NULL,
                                       `description` TEXT,
                                       `type` INTEGER NOT NULL
                                   );""")
        self._connection.commit()
        # select * from sqlite_master where type='table';

    @property
    def date_format(self):
        """
        Returns the date format.
        :return: The date format.
        """
        return self._date_format

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

    def get_user_uid(self, name):
        """
        Returns the uid of the given user, or None if the name does not exist.
        :param name: The name.
        :return: The uid.
        """
        assert isinstance(name, str)
        uid = None
        c = self._connection.cursor()
        c.execute("SELECT `uid` FROM Users WHERE `name`=?;", (name,))
        result = c.fetchone()
        if result is not None:
            uid = result[0]
        return uid

    def get_or_create_user_uid(self, name):
        """
        Returns the uid of the given user. If the name does not exist, it will be inserted.
        :param name: The name.
        :return: The uid.
        """
        assert isinstance(name, str)
        uid = self.get_user_uid(name)
        if uid is None:
            c = self._connection.cursor()
            c.execute("INSERT INTO Users (`name`) VALUES (?);", (name,))
            self._connection.commit()
            uid = c.lastrowid
        return uid

    def set_setting(self, user_uid, key, value):
        """
        Adds a setting entry to the database. Throws a TypeError if value cannot be converted to JSON via json.dumps.
        :param user_uid: The user uid.
        :param key: The setting key.
        :param value: The setting value.
        """
        assert isinstance(user_uid, int)
        assert isinstance(key, str)
        s = json.dumps(value)
        timestamp = self._get_current_timestamp()
        c = self._connection.cursor()
        c.execute("INSERT INTO Settings (`user_uid`, `timestamp_create`, `key`, `value`) VALUES (?, ?, ?, ?);",
                  (user_uid, timestamp, key, s))

    def get_setting(self, user_uid, key, default=None):
        """
        Returns the setting value for the given user.
        If there is no stored setting entry and default is set, default is returned. If there is no stored setting entry
        and default is not set, a KeyError is thrown.
        :param user_uid: The user uid.
        :param key: The setting key.
        :param default: The default value.
        :return: The setting value.
        """
        assert isinstance(user_uid, int)
        assert isinstance(key, str)
        c = self._connection.cursor()
        c.execute("SELECT `timestamp_create`, `value` FROM Settings WHERE `user_uid`=? AND `key`=? "
                  "ORDER BY `timestamp_create` DESC;", (user_uid, key))
        row = c.fetchone()
        value = default
        if row is not None:
            value = json.loads(row[1])
        elif default is None:
            raise KeyError("Not setting found with user_uid=%s and key=%s." % (user_uid, key))
        return value

    def _get_current_timestamp(self):
        """
        Returns a well-formatted current timestamp.
        :return: The timestamp.
        """
        now = datetime.datetime.now()
        return now.strftime(self.date_format)
