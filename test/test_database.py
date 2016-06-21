import os
import unittest

from core.database_connector import DatabaseConnector


DB_PATH = "test.db"
db = None


def setUpModule():
    """
    Create the database.
    :return:
    """
    global db
    db = DatabaseConnector(DB_PATH)


def tearDownModule():
    """
    Remove the database file.
    """
    db.close()
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)


class TestDatabase(unittest.TestCase):

    def test_create_user(self):
        """
        Create multiple users and make sure that the uids different and greater than zero.
        """
        uid0 = db.get_user_uid("Martin")
        uid1 = db.get_user_uid("Peter")
        self.assertGreater(uid0, 0)
        self.assertGreater(uid1, 0)
        self.assertNotEqual(uid0, uid1)


if __name__ == "__main__":
    unittest.main()
