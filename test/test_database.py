import os
import unittest

from core.database_connector import DatabaseConnector
from core.database_types import User, Setting, Task, TrackEntry


DB_PATH = "test.db"
db = None


def setUpModule():
    """
    Create the database.
    """
    global db
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)
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
        Create multiple users and make sure that the uids differ.
        """
        user0 = User(name="Martin")
        user1 = User(name="Peter")
        db.create_user(user0)
        db.create_user(user1)
        self.assertGreater(user0.uid, 0)
        self.assertGreater(user1.uid, 0)
        self.assertNotEqual(user0.uid, user1.uid)

    def test_get_user(self):
        """
        Check that the uid is consistent between create_user() and get_user().
        """
        user0 = User(name="Abel")
        with self.assertRaises(KeyError):
            user1 = db.get_user(user0.name)
        db.create_user(user0)
        user1 = db.get_user(user0.name)
        self.assertEqual(user0, user1)

    def test_update_user(self):
        """
        Create and update a user and make sure that the uid remains the same and that only the updated values are found.
        """
        # Insert a user and get the uid.
        user0 = User(name="Stefan")
        db.create_user(user0)
        uid = user0.uid

        # Perform an update.
        user0.name = "Stephan"
        db.update_user(user0)

        # Check that the updated user has the same uid and that the old user is not found anymore.
        user1 = db.get_user("Stephan")
        self.assertEqual(uid, user1.uid)
        with self.assertRaises(KeyError):
            user2 = db.get_user("Stefan")

    def test_create_setting(self):
        """
        Create settings for different users and with different keys and make sure that the uids differ.
        """
        user0 = User(name="Adam")
        user1 = User(name="Eva")
        db.create_user(user0)
        db.create_user(user1)
        setting0 = Setting(user_uid=user0.uid, key="testkey0", value=2)
        setting1 = Setting(user_uid=user0.uid, key="testkey1", value=2)
        setting2 = Setting(user_uid=user1.uid, key="testkey0", value=2)
        for s in (setting0, setting1, setting2):
            db.create_setting(s)
        for s in (setting0, setting1, setting2):
            self.assertGreater(s.uid, 0)
        self.assertNotEqual(setting0.uid, setting1.uid)
        self.assertNotEqual(setting0.uid, setting2.uid)
        self.assertNotEqual(setting1.uid, setting2.uid)

    def test_get_setting(self):
        """
        Check that get_setting() works as expected.
        """
        user = User(name="Thomas")
        db.create_user(user)

        with self.assertRaises(KeyError):
            setting = db.get_setting(user.uid, "testkey")

        setting0 = Setting(user_uid=user.uid, key="testkey", value=7)
        db.create_setting(setting0)
        setting1 = db.get_setting(user.uid, "testkey")
        self.assertEqual(setting0, setting1)

        setting2 = Setting(user_uid=user.uid, key="testkey", value=8)
        db.create_setting(setting2)
        setting3 = db.get_setting(user.uid, "testkey")
        self.assertEqual(setting2, setting3)
        self.assertNotEqual(setting0, setting3)

    def test_create_task(self):
        """
        Create tasks for different users and make sure that the uids differ.
        """
        user0 = User(name="Moritz")
        user1 = User(name="Alex")
        db.create_user(user0)
        db.create_user(user1)
        task0 = Task(user_uid=user0.uid, type_id=0)
        task1 = Task(user_uid=user1.uid, type_id=0)
        for t in (task0, task1):
            db.create_task(t)
        for t in (task0, task1):
            self.assertGreater(t.uid, 0)
        self.assertNotEqual(task0.uid, task1.uid)

    def test_get_all_tasks(self):
        """
        Create tasks for different users and make sure that get_all_tasks() only returns the tasks for the given user.
        """
        user0 = User(name="Harald")
        user1 = User(name="Philippe")
        db.create_user(user0)
        db.create_user(user1)
        tasks0 = [Task(user_uid=user0.uid, type_id=0) for _ in range(3)]
        tasks1 = [Task(user_uid=user1.uid, type_id=0) for _ in range(5)]
        for t in tasks0 + tasks1:
            db.create_task(t)
        tasks2 = db.get_all_tasks(user0.uid)
        tasks3 = db.get_all_tasks(user1.uid)
        self.assertEqual(tasks0, tasks2)
        self.assertNotEqual(tasks0, tasks3)
        self.assertNotEqual(tasks1, tasks2)
        self.assertEqual(tasks1, tasks3)

    def test_get_open_tasks(self):
        """
        Create finished and unfinished tasks and check that get_open_tasks() only returns the unfinished tasks.
        """
        user = User(name="Friedrich")
        db.create_user(user)
        tasks0 = [Task(user_uid=user.uid, type_id=0, done=True) for _ in range(3)]
        tasks1 = [Task(user_uid=user.uid, type_id=0) for _ in range(5)]
        for t in tasks0 + tasks1:
            db.create_task(t)
        tasks2 = db.get_open_tasks(user.uid)
        self.assertNotEqual(tasks0, tasks2)
        self.assertEqual(tasks1, tasks2)

    def test_update_task(self):
        """
        Create and update a task and make sure that the uid remains the same and that only the updated values are found.
        """
        # Create a task.
        user = User(name="Mark")
        db.create_user(user)
        task0 = Task(user_uid=user.uid, type_id=0, title="Initial title")
        db.create_task(task0)
        uid = task0.uid

        # Perform an update.
        task0.title = "New title"
        db.update_task(task0)

        # Check that the updated task has the same uid and that the old task is not found anymore.
        tasks = db.get_all_tasks(user.uid)
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        self.assertEqual(task.uid, uid)
        self.assertEqual(task.title, "New title")

    def test_delete_task(self):
        """
        Create and delete a task and make sure that get_open_tasks() and get_all_tasks() do not return the deleted task.
        """
        user = User(name="Sebastian")
        db.create_user(user)
        tasks = [Task(user_uid=user.uid, type_id=0) for _ in range(5)]
        for t in tasks:
            db.create_task(t)
        task = tasks.pop(1)
        task.deleted = True
        db.update_task(task)
        open_tasks = db.get_open_tasks(user.uid)
        all_tasks = db.get_all_tasks(user.uid)
        self.assertEqual(open_tasks, tasks)
        self.assertEqual(all_tasks, tasks)

    def test_create_track_entry(self):
        """
        Create track entries and make sure that the uids differ.
        """
        task = Task(user_uid=1, type_id=0)
        db.create_task(task)
        now = db.get_current_timestamp()
        entry0 = TrackEntry(task_uid=task.uid, timestamp_begin=now, timestamp_end=now)
        entry1 = TrackEntry(task_uid=task.uid, timestamp_begin=now, timestamp_end=now)
        for entry in (entry0, entry1):
            db.create_track_entry(entry)
        for entry in (entry0, entry1):
            self.assertGreater(entry.uid, 0)

    def test_get_track_entries_for_task(self):
        """
        Create track entries for different tasks and make sure that get_all_tasks() only returns the entries for the
        given task.
        """
        task0 = Task(user_uid=2, type_id=0)
        task1 = Task(user_uid=2, type_id=0)
        db.create_task(task0)
        db.create_task(task1)
        now = db.get_current_timestamp()
        entries0 = [TrackEntry(task_uid=task0.uid, timestamp_begin=now, timestamp_end=now) for _ in range(3)]
        entries1 = [TrackEntry(task_uid=task1.uid, timestamp_begin=now, timestamp_end=now) for _ in range(5)]
        for entry in entries0 + entries1:
            db.create_track_entry(entry)
        entries2 = db.get_track_entries_for_task(task0.uid)
        entries3 = db.get_track_entries_for_task(task1.uid)
        self.assertEqual(entries0, entries2)
        self.assertNotEqual(entries0, entries3)
        self.assertNotEqual(entries1, entries2)
        self.assertEqual(entries1, entries3)

    def test_update_track_entry(self):
        """
        Create and update a track entry and make sure that the uid remains the same and that only the updated values are
        found.
        """
        # Create a track entry.
        user = User(name="Heinz")
        db.create_user(user)
        task = Task(user_uid=user.uid, type_id=0)
        db.create_task(task)
        entry0 = TrackEntry(task_uid=task.uid, timestamp_begin=db.get_current_timestamp())
        db.create_track_entry(entry0)
        uid = entry0.uid

        # Perform an update.
        entry0.timestamp_begin = "some text"
        db.update_track_entry(entry0)

        # Check that the updated track entry has the same uid and that the old track entry is not found anymore.
        entries = db.get_track_entries_for_task(task.uid)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.uid, uid)
        self.assertEqual(entry.timestamp_begin, "some text")


if __name__ == "__main__":
    unittest.main()
