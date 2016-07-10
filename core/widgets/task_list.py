import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

from ..common import log_exceptions
from ..user_management import UserManagement
from .delete_task_dialog import DeleteTaskDialog
from .task_widget import TaskWidget


class TaskList(QGroupBox):
    """
    The TaskList is a GroupBox that shows a list of TaskWidgets and handles the connections of the tasks to the user
    management.
    """

    def __init__(self, user_management, *args, **kwargs):
        super().__init__(title="Open Tasks", *args, **kwargs)

        assert isinstance(user_management, UserManagement)

        self._user_management = user_management
        self._tasks = {}  # map with the tasks {task_uid: TaskWidget}

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def load_open_tasks(self):
        """
        Load the open user tasks.
        """
        for task in self._user_management.open_tasks:
            self.add_task(task.uid, task.title, task.description)

    @pyqtSlot(int, str, str)
    @log_exceptions
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
            task.delete.connect(self._on_show_delete_task_dialog)
            task.start.connect(self._on_start_task)
            task.stop.connect(self._on_stop_task)
            task.done.connect(self._on_task_done)
            self.layout.addWidget(task)
            self._tasks[task_uid] = task

    @pyqtSlot(int, name="_on_show_delete_task_dialog")
    @log_exceptions
    def _on_show_delete_task_dialog(self, task_uid):
        title = self._tasks[task_uid].title
        w = DeleteTaskDialog(task_uid, title, parent=self)
        w.accepted.connect(self._on_delete_task)
        w.show()

    @pyqtSlot(int, name="_on_delete_task")
    @log_exceptions
    def _on_delete_task(self, task_uid):
        task = self._tasks.pop(task_uid)
        task.deleteLater()
        self._user_management.delete_task(task_uid)

    @pyqtSlot(int, name="_on_start_task")
    @log_exceptions
    def _on_start_task(self, task_uid):
        logging.debug("Start work on task " + str(task_uid))

    @pyqtSlot(int, name="_on_stop_task")
    @log_exceptions
    def _on_stop_task(self, task_uid):
        logging.debug("Stop work on task " + str(task_uid))

    @pyqtSlot(int, name="_on_task_done")
    @log_exceptions
    def _on_task_done(self, task_uid):
        task = self._tasks.pop(task_uid)
        task.deleteLater()
        self._user_management.task_done(task_uid)
