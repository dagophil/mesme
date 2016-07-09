from .database_connector import DatabaseConnector
from .database_types import User


class UserManagement(object):

    def __init__(self, user_name, database_location):
        self._user = User(name=user_name)
        self._database = DatabaseConnector(database_location)
        self._database.create_user(self._user)
        self.open_tasks = self._database.get_open_tasks(self._user.uid)
