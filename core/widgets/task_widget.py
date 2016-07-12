from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSizePolicy

from ..common import log_exceptions


class TaskWidget(QWidget):
    """
    The TaskWidget is a QWidget with two labels and three buttons. It is used to show title and description of a task
    and provides signals to start and stop the time tracking for that task.
    """

    delete = pyqtSignal(int, name="delete")
    start = pyqtSignal(int, name="start")
    stop = pyqtSignal(int, name="stop")
    done = pyqtSignal(int, name="done")

    def __init__(self, task_uid, title, description, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = title
        self._task_uid = task_uid
        self._started = False

        # Create the layout.
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Set the title format.
        title = "<b>%s</b>" % title

        # Create the labels and the buttons.
        delete_btn = QPushButton(text="Delete")
        delete_btn.clicked.connect(self._clicked_delete)
        title_lbl = QLabel(text=title)
        description_lbl = QLabel(text=description)
        description_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.toggle_btn = QPushButton(text="Start")
        self.toggle_btn.clicked.connect(self._clicked_toggle)
        done_btn = QPushButton(text="Done")
        done_btn.clicked.connect(self._clicked_done)

        for widget in (delete_btn, title_lbl, description_lbl, self.toggle_btn, done_btn):
            layout.addWidget(widget)

    @property
    def started(self):
        return self._started

    def start_task(self):
        self._started = True
        self.toggle_btn.setText("Stop")
        self.start.emit(self._task_uid)

    def stop_task(self):
        self._started = False
        self.toggle_btn.setText("Start")
        self.stop.emit(self._task_uid)

    @pyqtSlot(bool, name="_clicked_delete")
    @log_exceptions
    def _clicked_delete(self, b):
        self.delete.emit(self._task_uid)

    @pyqtSlot(bool, name="_clicked_toggle")
    @log_exceptions
    def _clicked_toggle(self, b):
        if self._started:
            self.stop_task()
        else:
            self.start_task()

    @pyqtSlot(bool, name="_clicked_done")
    @log_exceptions
    def _clicked_done(self, b):
        self.done.emit(self._task_uid)
