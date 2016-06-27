import os
import unittest

from core.database_connector import DatabaseConnector


DB_PATH = "test.db"
db = None


def setUpModule():
    """
    Create the database.
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
        uid0 = db.get_or_create_user_uid("Martin")
        uid1 = db.get_or_create_user_uid("Peter")
        self.assertGreater(uid0, 0)
        self.assertGreater(uid1, 0)
        self.assertNotEqual(uid0, uid1)

    def test_get_user_uid(self):
        """
        Check that the uid is consistent between get_or_create_user_uid() and get_user_uid().
        """
        uid0 = db.get_or_create_user_uid("Hans")
        uid1 = db.get_user_uid("Hans")
        self.assertGreater(uid0, 0)
        self.assertEqual(uid0, uid1)

    def test_settings(self):
        """
        Check the get and set settings functions.
        """
        uid = db.get_or_create_user_uid("Thomas")
        with self.assertRaises(KeyError):
            value = db.get_setting(uid, "testkey")
        value = db.get_setting(uid, "testkey", default=5)
        self.assertEqual(value, 5)
        db.set_setting(uid, "testkey", 2)
        value = db.get_setting(uid, "testkey")
        self.assertEqual(value, 2)
        value = db.get_setting(uid, "testkey", default=5)
        self.assertEqual(value, 2)
        db.set_setting(uid, "testkey", 6)
        value = db.get_setting(uid, "testkey")
        self.assertEqual(value, 6)


if __name__ == "__main__":
    unittest.main()
