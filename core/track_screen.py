import logging

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QVBoxLayout, QPushButton, QSizePolicy

from .common import log_exceptions
from .create_task_dialog import CreateTaskDialog
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
        tracking_controls.create_task.connect(self._on_show_create_task_dialog)
        tracking_controls.general_work.connect(self._on_general_work)
        tracking_controls.pause.connect(self._on_pause)
        tracking_controls.end_of_work.connect(self._on_end_of_work)

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
            task.start.connect(self._on_start_task)
            task.stop.connect(self._on_stop_task)
            task.done.connect(self._on_task_done)
            self._task_box.addWidget(task)
            self._tasks[task_uid] = task

    @pyqtSlot(name="_on_show_create_task_dialog")
    @log_exceptions
    def _on_show_create_task_dialog(self):
        """
        Show the create task dialog.
        """
        w = CreateTaskDialog(parent=self)
        w.accepted.connect(self._on_create_task)
        w.show()

    @pyqtSlot(tuple, name="_on_create_task")
    @log_exceptions
    def _on_create_task(self, task_values):
        """
        Create the task.
        """
        logging.debug("Creating task " + str(task_values))

    @pyqtSlot(name="_on_general_work")
    @log_exceptions
    def _on_general_work(self):
        """
        Start general work.
        """
        logging.debug("Starting general work")

    @pyqtSlot(name="_on_pause")
    @log_exceptions
    def _on_pause(self):
        """
        Start pause.
        """
        logging.debug("Pause")

    @pyqtSlot(name="_on_end_of_work")
    @log_exceptions
    def _on_end_of_work(self):
        """
        Stop the work for today.
        """
        logging.debug("End of work")

    @pyqtSlot(int, name="_on_start_task")
    @log_exceptions
    def _on_start_task(self, task_uid):
        """
        Start the time tracking on the task with the given uid.
        :param task_uid: The task uid.
        """
        logging.debug("Start work on task " + str(task_uid))

    @pyqtSlot(int, name="_on_stop_task")
    @log_exceptions
    def _on_stop_task(self, task_uid):
        """
        Stop the time tracking on the task with the given uid.
        :param task_uid: The task uid.
        """
        logging.debug("Stop work on task " + str(task_uid))

    @pyqtSlot(int, name="_on_task_done")
    @log_exceptions
    def _on_task_done(self, task_uid):
        """
        Set the task with the given uid to done.
        :param task_uid:  The task uid.
        """
        logging.debug("Setting task " + str(task_uid) + " to done")
