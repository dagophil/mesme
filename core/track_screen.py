import logging

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .common import log_exceptions
from .user_management import UserManagement
from .user_profile import UserProfile
from .widgets import TaskList, TrackingControls


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
        self._task_list = TaskList()
        self._task_list.load_open_tasks(self._user_management)
        self._task_list.delete.connect(self._on_delete_task)
        self._task_list.start.connect(self._on_start_task)
        self._task_list.stop.connect(self._on_stop_task)
        self._task_list.done.connect(self._on_task_done)

        # Create the tracking controls.
        self._tracking_controls = TrackingControls()
        self._tracking_controls.create_task.connect(self._on_create_task)
        self._tracking_controls.general_work.connect(self._on_general_work)
        self._tracking_controls.pause.connect(self._on_pause)
        self._tracking_controls.end_of_work.connect(self._on_end_of_work)

        # Create the layout.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        layout.addWidget(self._tracking_controls)
        layout.addWidget(self._task_list)

    @pyqtSlot(str, str, name="_on_create_task")
    @log_exceptions
    def _on_create_task(self, title, description):
        uid = self._user_management.create_task(title, description)
        self._task_list.add_task(uid, title, description)

    @pyqtSlot(int, name="_on_delete_task")
    @log_exceptions
    def _on_delete_task(self, task_uid):
        self._user_management.delete_task(task_uid)
        self._task_list.remove_task(task_uid)

    @pyqtSlot(int, name="_on_start_task")
    @log_exceptions
    def _on_start_task(self, task_uid):
        if self._user_management.current_task_uid is not None:
            self._on_stop_task(self._user_management.current_task_uid)
        self._user_management.start_task(task_uid)
        self._task_list.start_task(task_uid)
        self._tracking_controls.enable_pause_button()
        self._tracking_controls.enable_general_work_button()

    @pyqtSlot(int, name="_on_stop_task")
    @log_exceptions
    def _on_stop_task(self, task_uid):
        assert task_uid == self._user_management.current_task_uid
        self._user_management.stop_current_task()
        self._task_list.stop_task(task_uid)
        self._tracking_controls.disable_pause_button()
        self._tracking_controls.enable_general_work_button()

    @pyqtSlot(int, name="_on_task_done")
    @log_exceptions
    def _on_task_done(self, task_uid):
        if self._user_management.current_task_uid == task_uid:
            self._on_stop_task(task_uid)
        self._user_management.task_done(task_uid)
        self._task_list.remove_task(task_uid)

    @pyqtSlot(name="_on_general_work")
    @log_exceptions
    def _on_general_work(self):
        """
        Start general work.
        """
        task_uid = self._user_management.create_general_work_task()
        self._on_start_task(task_uid)
        self._tracking_controls.disable_general_work_button()

    @pyqtSlot(name="_on_pause")
    @log_exceptions
    def _on_pause(self):
        """
        Start pause.
        """
        task_uid = self._user_management.create_pause_task()
        self._on_start_task(task_uid)
        self._tracking_controls.disable_pause_button()

    @pyqtSlot(name="_on_end_of_work")
    @log_exceptions
    def _on_end_of_work(self):
        """
        Stop the work for today.
        """
        if self._user_management.current_task_uid is not None:
            self._on_stop_task(self._user_management.current_task_uid)
