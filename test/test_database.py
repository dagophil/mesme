import os
import unittest

from core.database_connector import DatabaseConnector
from core.database_types import User, Setting, Task, TrackEntry


DB_PATH = "test.db"
db = None


class TestDatabase(unittest.TestCase):

    def setUp(self):
        global db
        if os.path.isfile(DB_PATH):
            os.remove(DB_PATH)
        db = DatabaseConnector(DB_PATH)

    def tearDown(self):
        db.close()
        if os.path.isfile(DB_PATH):
            os.remove(DB_PATH)

    def test_create_user(self):
        """
        Create multiple users and make sure that the uids differ.
        """
        users = [User(name=name) for name in ("Martin", "Peter", "Stefan", "Hans", "Jakob")]
        for u in users:
            db.create_user(u)
        uids = set(user.uid for user in users)
        self.assertEqual(len(uids), len(users))
        for uid in uids:
            self.assertGreater(uid, 0)

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
        settings0 = [Setting(user_uid=1, key="testkey%d"%i, value=2) for i in range(3)]
        settings1 = [Setting(user_uid=2, key="testkey%d"%i, value=2) for i in range(5)]
        settings = settings0 + settings1
        for s in settings:
            db.create_setting(s)
        uids = set(setting.uid for setting in settings)
        self.assertEqual(len(uids), len(settings))
        for uid in uids:
            self.assertGreater(uid, 0)

    def test_get_setting(self):
        """
        Check that get_setting() works as expected.
        """
        user_uid = 1
        with self.assertRaises(KeyError):
            setting = db.get_setting(user_uid, "testkey")

        setting0 = Setting(user_uid=user_uid, key="testkey", value=7)
        db.create_setting(setting0)
        setting1 = db.get_setting(user_uid, "testkey")
        self.assertEqual(setting0, setting1)

        setting2 = Setting(user_uid=user_uid, key="testkey", value=8)
        db.create_setting(setting2)
        setting3 = db.get_setting(user_uid, "testkey")
        self.assertEqual(setting2, setting3)
        self.assertNotEqual(setting0, setting3)

    def test_create_task(self):
        """
        Create tasks and make sure that the uids differ.
        """
        tasks0 = [Task(user_uid=1, type_id=0) for _ in range(3)]
        tasks1 = [Task(user_uid=2, type_id=0) for _ in range(5)]
        tasks = tasks0 + tasks1
        for t in tasks:
            db.create_task(t)
        uids = set(task.uid for task in tasks)
        self.assertEqual(len(uids), len(tasks))  # make sure that all uids are different
        for uid in uids:
            self.assertGreater(uid, 0)

    def test_get_all_tasks(self):
        """
        Create tasks for different users and make sure that get_all_tasks() only returns the tasks for the given user.
        """
        user0_uid = 1
        user1_uid = 2
        tasks0 = [Task(user_uid=user0_uid, type_id=0) for _ in range(3)]
        tasks1 = [Task(user_uid=user1_uid, type_id=0) for _ in range(5)]
        for t in tasks0 + tasks1:
            db.create_task(t)
        tasks2 = db.get_all_tasks(user0_uid)
        tasks3 = db.get_all_tasks(user1_uid)
        self.assertEqual(tasks0, tasks2)
        self.assertNotEqual(tasks0, tasks3)
        self.assertNotEqual(tasks1, tasks2)
        self.assertEqual(tasks1, tasks3)

    def test_get_open_tasks(self):
        """
        Create finished and unfinished tasks and check that get_open_tasks() only returns the unfinished tasks.
        """
        user_uid = 1
        tasks0 = [Task(user_uid=user_uid, type_id=0, done=True) for _ in range(3)]
        tasks1 = [Task(user_uid=user_uid, type_id=0) for _ in range(5)]
        for t in tasks0 + tasks1:
            db.create_task(t)
        tasks2 = db.get_open_tasks(user_uid)
        self.assertEqual(tasks1, tasks2)
        self.assertNotEqual(tasks0, tasks2)

    def test_update_task(self):
        """
        Create and update a task and make sure that the uid remains the same and that only the updated values are found.
        """
        # Create a task.
        user_uid = 1
        task0 = Task(user_uid=user_uid, type_id=0, title="Initial title")
        db.create_task(task0)
        uid = task0.uid

        # Perform an update.
        task0.title = "New title"
        db.update_task(task0)

        # Check that the updated task has the same uid and that the old task is not found anymore.
        tasks = db.get_all_tasks(user_uid)
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        self.assertEqual(task.uid, uid)
        self.assertEqual(task.title, "New title")

    def test_delete_task(self):
        """
        Create and delete a task and make sure that get_open_tasks() and get_all_tasks() do not return the deleted task.
        """
        user_uid = 1
        tasks = [Task(user_uid=user_uid, type_id=0) for _ in range(5)]
        for t in tasks:
            db.create_task(t)
        task = tasks.pop(1)
        task.deleted = True
        db.update_task(task)
        open_tasks = db.get_open_tasks(user_uid)
        all_tasks = db.get_all_tasks(user_uid)
        self.assertEqual(open_tasks, tasks)
        self.assertEqual(all_tasks, tasks)

    def test_create_track_entry(self):
        """
        Create track entries and make sure that the uids differ.
        """
        now = db.get_current_timestamp()
        entries0 = [TrackEntry(task_uid=1, timestamp_begin=now, timestamp_end=now) for _ in range(3)]
        entries1 = [TrackEntry(task_uid=2, timestamp_begin=now, timestamp_end=now) for _ in range(8)]
        entries = entries0 + entries1
        for e in entries:
            db.create_track_entry(e)
        uids = set(entry.uid for entry in entries)
        self.assertEqual(len(uids), len(entries))
        for uid in uids:
            self.assertGreater(uid, 0)

    def test_get_track_entries(self):
        """
        Create track entries for different tasks and make sure that get_all_tasks() only returns the entries for the
        given task.
        """
        task0_uid = 1
        task1_uid = 2
        now = db.get_current_timestamp()
        entries0 = [TrackEntry(task_uid=task0_uid, timestamp_begin=now, timestamp_end=now) for _ in range(3)]
        entries1 = [TrackEntry(task_uid=task1_uid, timestamp_begin=now, timestamp_end=now) for _ in range(5)]
        for entry in entries0 + entries1:
            db.create_track_entry(entry)
        entries2 = db.get_track_entries(task0_uid)
        entries3 = db.get_track_entries(task1_uid)
        self.assertEqual(entries0, entries2)
        self.assertNotEqual(entries0, entries3)
        self.assertNotEqual(entries1, entries2)
        self.assertEqual(entries1, entries3)

    def test_get_open_track_entries_for_task(self):
        """
        Create open and closed track entries and make sure that get_open_track_entries_for_task() only returns the open
        track entries.
        """
        task_uid = 1
        now = db.get_current_timestamp()
        entries0 = [TrackEntry(task_uid=task_uid, timestamp_begin=now, timestamp_end=now) for _ in range(3)]
        entries1 = [TrackEntry(task_uid=task_uid, timestamp_begin=now) for _ in range(5)]
        for e in entries0 + entries1:
            db.create_track_entry(e)
        entries2 = db.get_open_track_entries(task_uid)
        self.assertEqual(entries1, entries2)
        self.assertNotEqual(entries0, entries2)

    def test_update_track_entry(self):
        """
        Create and update a track entry and make sure that the uid remains the same and that only the updated values are
        found.
        """
        # Create a task.
        task_uid = 1
        entry0 = TrackEntry(task_uid=task_uid, timestamp_begin=db.get_current_timestamp())
        db.create_track_entry(entry0)
        uid = entry0.uid

        # Perform an update.
        entry0.timestamp_begin = "some text"
        db.update_track_entry(entry0)

        # Check that the updated track entry has the same uid and that the old track entry is not found anymore.
        entries = db.get_track_entries(task_uid)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.uid, uid)
        self.assertEqual(entry.timestamp_begin, "some text")


if __name__ == "__main__":
    unittest.main()
