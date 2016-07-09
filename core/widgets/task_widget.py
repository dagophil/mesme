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

        self._task_uid = task_uid
        self.title = title

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
        start_btn = QPushButton(text="Start")
        start_btn.clicked.connect(self._clicked_start)
        stop_btn = QPushButton(text="Stop")
        stop_btn.clicked.connect(self._clicked_stop)
        done_btn = QPushButton(text="Done")
        done_btn.clicked.connect(self._clicked_done)

        for widget in (delete_btn, title_lbl, description_lbl, start_btn, stop_btn, done_btn):
            layout.addWidget(widget)

    @pyqtSlot(bool, name="_clicked_delete")
    @log_exceptions
    def _clicked_delete(self, b):
        self.delete.emit(self._task_uid)

    @pyqtSlot(bool, name="_clicked_start")
    @log_exceptions
    def _clicked_start(self, b):
        self.start.emit(self._task_uid)

    @pyqtSlot(bool, name="_clicked_stop")
    @log_exceptions
    def _clicked_stop(self, b):
        self.stop.emit(self._task_uid)

    @pyqtSlot(bool, name="_clicked_done")
    @log_exceptions
    def _clicked_done(self, b):
        self.done.emit(self._task_uid)
