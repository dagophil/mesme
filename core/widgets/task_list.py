import logging

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

from ..common import log_exceptions
from .delete_task_dialog import DeleteTaskDialog
from .task_widget import TaskWidget


class TaskList(QGroupBox):
    """
    The TaskList is a GroupBox that shows a list of TaskWidgets and handles the connections of the tasks to the user
    management.
    """

    delete = pyqtSignal(int, name="delete")
    start = pyqtSignal(int, name="start")
    stop = pyqtSignal(int, name="stop")
    done = pyqtSignal(int, name="done")

    def __init__(self, *args, **kwargs):
        super().__init__(title="Open Tasks", *args, **kwargs)

        self._tasks = {}  # map with the tasks {task_uid: TaskWidget}
        self._current_track_entry_uid = None

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def load_open_tasks(self, user_management):
        for task in user_management.get_open_tasks():
            self.add_task(task.uid, task.title, task.description)

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
            task.start.connect(self.start)
            task.stop.connect(self.stop)
            task.done.connect(self.done)
            self.layout.addWidget(task)
            self._tasks[task_uid] = task

    def remove_task(self, task_uid):
        task = self._tasks.pop(task_uid)
        task.deleteLater()

    def start_task(self, task_uid):
        if task_uid in self._tasks:
            self._tasks[task_uid].start_task()

    def stop_task(self, task_uid):
        if task_uid in self._tasks:
            self._tasks[task_uid].stop_task()

    @pyqtSlot(int, name="_on_show_delete_task_dialog")
    @log_exceptions
    def _on_show_delete_task_dialog(self, task_uid):
        title = self._tasks[task_uid].title
        w = DeleteTaskDialog(task_uid, title, parent=self)
        w.accepted.connect(self.delete)
        w.show()
