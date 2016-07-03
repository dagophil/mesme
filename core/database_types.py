from collections import OrderedDict


def create_table(connection, table_name, database_object_class, if_not_exists=False):
    """
    Create the database table for the given database object class.
    :param connection: The database connection.
    :param table_name: The table name.
    :param database_object_class: The database object class.
    :param if_not_exists: Whether the IF NOT EXISTS clause should be added.
    """
    assert issubclass(database_object_class, DatabaseObject)
    if_not_exists_str = " IF NOT EXISTS" if if_not_exists else ""
    field_types = database_object_class._field_types
    column_list = ["`%s` %s" % (name, sql_type) for name, sql_type in field_types.items()]
    columns = ", ".join(column_list)
    query = "CREATE TABLE%s `%s` (%s);" % (if_not_exists_str, table_name, columns)
    c = connection.cursor()
    c.execute(query)
    connection.commit()


def insert_object(connection, table_name, database_object):
    """
    Insert the given database object into the database. Sets database_object.uid.
    :param connection: The database connection.
    :param table_name: The table name.
    :param database_object: The database object.
    """
    assert isinstance(database_object, DatabaseObject)
    database_object.uid = None
    values = database_object.field_values()
    sql_placeholder = ", ".join("?" for _ in values)
    query = "INSERT INTO `%s` VALUES (%s);" % (table_name, sql_placeholder)
    c = connection.cursor()
    c.execute(query, values)
    connection.commit()
    database_object.uid = c.lastrowid


def update_object(connection, table_name, database_object, ignore_none=False):
    """
    Get the database row with uid=database_object.uid and overwrite all row entries with the ones from database_object.
    If ignore_none is True, only the not-None fields of database_object are used.
    Raises a KeyError() if no row with the given uid exists.
    :param connection: The database connection.
    :param table_name: The table name.
    :param database_object: The database object.
    :param ignore_none: Whether None values should be ignored.
    """
    assert isinstance(database_object, DatabaseObject)
    assert isinstance(database_object.uid, int)

    # Build the list with the values that should be set.
    set_items = []
    set_values = []
    for column_name, value in database_object.field_items():
        ignore = ignore_none and value is None
        if column_name != "uid" and not ignore:
            set_items.append("`%s`=?" % column_name)
            set_values.append(value)

    # Perform the actual update.
    if len(set_items) > 0:
        set_str = ", ".join(set_items)
        query = "UPDATE `%s` SET %s WHERE `uid`=?;" % (table_name, set_str)
        values = tuple(set_values) + (database_object.uid,)
        c = connection.cursor()
        c.execute(query, values)
        connection.commit()


class DatabaseObject(object):
    """
    Base class for all database objects.
    """

    """
    Ordered dict with the column names and types of the database object. Key is the column name, value is the sql type.
    Must be set in the subclass.
    Example:
    _field_types = OrderedDict([
        ("uid", "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"),
        ("name", "TEXT NOT NULL"}
    ])
    """
    _field_types = None

    def __init__(self):
        """
        Initialize the all fields with None.
        """
        if self._field_types is None:
            raise RuntimeError("Tried to initialize DatabaseObject without columns.")
        self._field_values = OrderedDict()
        for name in self._field_types:
            self._field_values[name] = None

    def field_items(self):
        """
        Returns the column name and value of the database object as odict_items.
        The return value can be used similar to d.items(), where d is a dict.
        :return: Column name and according value.
        """
        return self._field_values.items()

    def field_values(self):
        """
        Returns the field values of the database object as a tuple.
        :return: The field values.
        """
        return tuple(self._field_values.values())

    def __getattr__(self, name):
        """
        Return the value of the column with the given name.
        :param name: The column name.
        :return: The column value.
        """
        return self._field_values[name]

    def __setattr__(self, key, value):
        """
        Set the value of the column with the given name.
        :param key: Column name.
        :param value: Column value.
        """
        if key == "_field_values":
            super().__setattr__(key, value)
        elif key in self._field_values:
            self._field_values[key] = value
        else:
            raise KeyError()

    def __eq__(self, other):
        """
        Returns True if the uid and all field values of self and other are equal.
        :param other: The other user object.
        :return: Whether self equals other.
        """
        if isinstance(other, self.__class__):
            return self.field_values() == other.field_values()
        else:
            return False


class User(DatabaseObject):
    """
    The user database object.
    """

    _field_types = OrderedDict([
        ("uid", "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"),
        ("name", "TEXT NOT NULL")
    ])

    def __init__(self, uid=None, name=None):
        """
        Initialize the user object.
        :param uid: The uid.
        :param name: The user name.
        """
        super().__init__()
        self.uid = uid
        self.name = name


class Setting(DatabaseObject):
    """
    The setting database object.
    """

    _field_types = OrderedDict([
        ("uid", "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"),
        ("user_uid", "INTEGER NOT NULL"),
        ("timestamp_create", "TEXT NOT NULL"),
        ("key", "TEXT NOT NULL"),
        ("value", "TEXT NOT NULL")
    ])

    def __init__(self, uid=None, user_uid=None, timestamp_create=None, key=None, value=None):
        """
        Initialize the settings object.
        :param uid: The uid.
        :param user_uid: The user uid.
        :param timestamp_create: Timestamp of creation.
        :param key: The setting key.
        :param value: The setting value.
        """
        super().__init__()
        self.uid = uid
        self.user_uid = user_uid
        self.timestamp_create = timestamp_create
        self.key = key
        self.value = value


class Task(DatabaseObject):
    """
    The task database object.
    """

    _field_types = OrderedDict([
        ("uid", "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"),
        ("user_uid", "INTEGER NOT NULL"),
        ("title", "TEXT"),
        ("description", "TEXT"),
        ("timestamp_create", "TEXT NOT NULL"),
        ("timestamp_done", "TEXT"),
        ("timestamp_orderby", "TEXT NOT NULL"),
        ("type_id", "INTEGER NOT NULL")
    ])

    def __init__(self, uid=None, user_uid=None, title=None, description=None, timestamp_create=None, timestamp_done=None,
                 timestamp_orderby=None, type_id=None):
        """
        Initialize the task object.
        :param uid: The uid.
        :param user_uid: The user uid.
        :param title: The title.
        :param description: The description.
        :param timestamp_create: Timestamp of creation.
        :param timestamp_done: Timestamp of completion.
        :param timestamp_orderby: Timestamp that is used for ordering.
        :param type_id: The type id.
        """
        super().__init__()
        self.uid = uid
        self.user_uid = user_uid
        self.title = title
        self.description = description
        self.timestamp_create = timestamp_create
        self.timestamp_done = timestamp_done
        self.timestamp_orderby = timestamp_orderby
        self.type_id = type_id


class TrackEntry(DatabaseObject):
    """
    The track entry database object.
    """

    _field_types = OrderedDict([
        ("uid", "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"),
        ("user_uid", "INTEGER NOT NULL"),
        ("task_uid", "INTEGER"),
        ("timestamp_begin", "TEXT NOT NULL"),
        ("timestamp_end", "TEXT NOT NULL"),
        ("description", "TEXT"),
        ("type_id", "INTEGER NOT NULL")
    ])

    def __init__(self, uid=None, user_uid=None, task_uid=None, datetime_begin=None, datetime_end=None, description=None,
                 type_id=None):
        """
        Initialize the track entry object.
        :param uid: The uid.
        :param user_uid: The user uid.
        :param task_uid: The task uid.
        :param datetime_begin: Timestamp of the beginning of the time tracking.
        :param datetime_end: Timestamp of the end of the time tracking.
        :param description: The description.
        :param type_id: The type id.
        """
        super().__init__()
        self.uid = uid
        self.user_uid = user_uid
        self.task_uid = task_uid
        self.datetime_begin = datetime_begin
        self.datetime_end = datetime_end
        self.description = description
        self.type_id = type_id
