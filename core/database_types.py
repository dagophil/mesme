from abc import ABCMeta, abstractmethod


class DatabaseObject(metaclass=ABCMeta):
    """
    Base class for all database objects.
    """

    def __init__(self, uid=None):
        """
        Initialize the database object.
        :param uid: The uid.
        """
        self.uid = uid

    @abstractmethod
    def field_values(self):
        """
        Returns the field values of the database object as a tuple.
        :return: The field values.
        """
        pass

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

    def __init__(self, uid=None, name=None):
        """
        Initialize the user object.
        :param uid: The uid.
        :param name: The user name.
        """
        super().__init__(uid=uid)
        self.name = name

    def field_values(self):
        """
        Returns the values of the user object as a tuple.
        :return: The tuple with the user values.
        """
        return self.uid, self.name,


class Setting(DatabaseObject):
    """
    The setting database object.
    """

    def __init__(self, uid=None, user_uid=None, timestamp_create=None, key=None, value=None):
        """
        Initialize the settings object.
        :param uid: The uid.
        :param user_uid: The user uid.
        :param timestamp_create: Timestamp of creation.
        :param key: The setting key.
        :param value: The setting value.
        """
        super().__init__(uid=uid)
        self.user_uid = user_uid
        self.timestamp_create = timestamp_create
        self.key = key
        self.value = value

    def field_values(self):
        """
        Returns the values of the settings object as a tuple.
        :return: The tuple with the setting values.
        """
        return self.uid, self.user_uid, self.timestamp_create, self.key, self.value


class Task(DatabaseObject):
    """
    The task database object.
    """

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
        super().__init__(uid=uid)
        self.user_uid = user_uid
        self.title = title
        self.description = description
        self.timestamp_create = timestamp_create
        self.timestamp_done = timestamp_done
        self.timestamp_orderby = timestamp_orderby
        self.type_id = type_id

    def field_values(self):
        """
        Returns the values of the task object as a tuple.
        :return: The tuple with the task values.
        """
        return (self.uid, self.user_uid, self.title, self.description, self.timestamp_create, self.timestamp_done,
                self.timestamp_orderby, self.type_id)


class TrackEntry(DatabaseObject):
    """
    The track entry database object.
    """

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
        super().__init__(uid=uid)
        self.user_uid = user_uid
        self.task_uid = task_uid
        self.datetime_begin = datetime_begin
        self.datetime_end = datetime_end
        self.description = description
        self.type_id = type_id
