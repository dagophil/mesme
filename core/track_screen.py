import logging

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QVBoxLayout, QPushButton, QSizePolicy

from .common import log_exceptions
from .user_management import UserManagement
from .user_profile import UserProfile
from .widgets import TaskWidget, TrackingControlsWidget


class TrackScreen(QWidget):

    def __init__(self, user_display_name, user_profile, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert isinstance(user_profile, UserProfile)

        # Initialize the user management.
        self._user_display_name = user_display_name
        db_user = user_profile["database_user_name"]
        db_location = user_profile["database_location"]
        self._user_management = UserManagement(db_user, db_location)

        # Create the widget layout.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Add the tracking controls.
        tracking_controls = TrackingControlsWidget()
        layout.addWidget(tracking_controls)
        tracking_controls.create_task.connect(self.on_create_task)
        tracking_controls.general_work.connect(self.on_general_work)
        tracking_controls.pause.connect(self.on_pause)
        tracking_controls.end_of_work.connect(self.on_end_of_work)

        # Add the task box.
        self._task_box = QVBoxLayout()
        self._task_box.setSpacing(0)
        task_group = QGroupBox(title="Open Tasks")
        layout.addWidget(task_group)
        task_group.setLayout(self._task_box)

        # Map with the tasks {task_uid: Task}.
        self._tasks = {}

    def add_task(self, task_uid, title, description):
        """
        Add the given task to the ui.
        :param task_uid: The task uid.
        :param title: The task title.
        :param description: The task description.
        """
        if task_uid in self._tasks:
            logging.warning("Tried to add a task to the track screen that was already added before.")
        else:
            task = TaskWidget(task_uid, title, description)
            task.start.connect(self.on_start_task)
            task.stop.connect(self.on_stop_task)
            task.done.connect(self.on_task_done)
            self._task_box.addWidget(task)
            self._tasks[task_uid] = task

    @pyqtSlot(name="on_create_task")
    @log_exceptions
    def on_create_task(self):
        """
        Show the create task dialog.
        """
        logging.debug("Creating task")

    @pyqtSlot(name="on_general_work")
    @log_exceptions
    def on_general_work(self):
        """
        Start general work.
        """
        logging.debug("Starting general work")

    @pyqtSlot(name="on_pause")
    @log_exceptions
    def on_pause(self):
        """
        Start pause.
        """
        logging.debug("Pause")

    @pyqtSlot(name="on_end_of_work")
    @log_exceptions
    def on_end_of_work(self):
        """
        Stop the work for today.
        """
        logging.debug("End of work")

    @pyqtSlot(int, name="on_start_task")
    @log_exceptions
    def on_start_task(self, task_uid):
        """
        Start the time tracking on the task with the given uid.
        :param task_uid: The task uid.
        """
        logging.debug("Start work on task " + str(task_uid))

    @pyqtSlot(int, name="on_stop_task")
    @log_exceptions
    def on_stop_task(self, task_uid):
        """
        Stop the time tracking on the task with the given uid.
        :param task_uid: The task uid.
        """
        logging.debug("Stop work on task " + str(task_uid))

    @pyqtSlot(int, name="on_task_done")
    @log_exceptions
    def on_task_done(self, task_uid):
        """
        Set the task with the given uid to done.
        :param task_uid:  The task uid.
        """
        logging.debug("Setting task " + str(task_uid) + " to done")
