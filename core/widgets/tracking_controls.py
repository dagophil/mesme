from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

from ..common import log_exceptions
from .create_task_dialog import CreateTaskDialog


class TrackingControls(QWidget):
    """
    The TrackingControlsWidget provides buttons to create tasks, start general work, pause, and end work.
    """

    create_task = pyqtSignal(int, str, str, name="create_task")
    general_work = pyqtSignal(name="general_work")
    pause = pyqtSignal(name="pause")
    end_of_work = pyqtSignal(name="end_of_work")

    def __init__(self, user_management, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user_management = user_management

        layout = QHBoxLayout()
        self.setLayout(layout)

        create_task_btn = QPushButton(text="Create task")
        create_task_btn.clicked.connect(self._clicked_create_task)
        general_work_btn = QPushButton(text="General work")
        general_work_btn.clicked.connect(self._clicked_general_work)
        pause_btn = QPushButton(text="Pause")
        pause_btn.clicked.connect(self._clicked_pause)
        end_of_work_btn = QPushButton(text="End of work")
        end_of_work_btn.clicked.connect(self._clicked_end_of_work)

        layout.addWidget(create_task_btn)
        layout.addStretch()
        for widget in (general_work_btn, pause_btn, end_of_work_btn):
            layout.addWidget(widget)

    @pyqtSlot(bool, name="_clicked_create_task")
    @log_exceptions
    def _clicked_create_task(self, b):
        w = CreateTaskDialog(parent=self)
        w.accepted.connect(self._on_create_task)
        w.show()

    @pyqtSlot(tuple, name="_on_create_task")
    @log_exceptions
    def _on_create_task(self, task_values):
        title, description = task_values
        uid = self._user_management.create_task(title, description)
        self.create_task.emit(uid, title, description)

    @pyqtSlot(bool, name="_clicked_general_work")
    @log_exceptions
    def _clicked_general_work(self, b):
        self.general_work.emit()

    @pyqtSlot(bool, name="_clicked_pause")
    @log_exceptions
    def _clicked_pause(self, b):
        self.pause.emit()

    @pyqtSlot(bool, name="_clicked_end_of_work")
    @log_exceptions
    def _clicked_end_of_work(self, b):
        self.end_of_work.emit()
