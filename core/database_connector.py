import logging
import sqlite3


class DatabaseConnector(object):

    def __init__(self, database_location):
        """
        Creates the database file and the necessary tables. If the database file already exists, it will not be
        overwritten.
        :param database_location: Path to the database.
        """
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
        Returns the uid of the given user. If the name does not exist, it will be inserted.
        :param name: The name.
        :return: The uid.
        """
        c = self._connection.cursor()
        c.execute("SELECT `uid` FROM Users WHERE `name`=?;", (name,))
        result = c.fetchone()
        if result is not None:
            uid = result[0]
        else:
            c.execute("INSERT INTO Users (`name`) VALUES (?);", (name,))
            self._connection.commit()
            uid = c.lastrowid
        return uid
