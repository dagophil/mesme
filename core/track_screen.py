import logging

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .common import log_exceptions
from .user_management import UserManagement
from .user_profile import UserProfile
from .widgets import CreateTaskDialog, TaskList, TrackingControls


class TrackScreen(QWidget):

    def __init__(self, user_display_name, user_profile, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert isinstance(user_profile, UserProfile)

        # Initialize the user management.
        self._user_display_name = user_display_name
        db_user = user_profile["database_user_name"]
        db_location = user_profile["database_location"]
        self._user_management = UserManagement(db_user, db_location)

        # Create the task box.
        self._task_list = TaskList(self._user_management)
        self._task_list.load_open_tasks()

        # Create the tracking controls.
        tracking_controls = TrackingControls(self._user_management)
        tracking_controls.create_task.connect(self._task_list.add_task)
        tracking_controls.general_work.connect(self._on_general_work)
        tracking_controls.pause.connect(self._on_pause)
        tracking_controls.end_of_work.connect(self._on_end_of_work)

        # Create the layout.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        layout.addWidget(tracking_controls)
        layout.addWidget(self._task_list)

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
