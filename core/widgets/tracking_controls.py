from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

from ..common import log_exceptions
from .create_task_dialog import CreateTaskDialog


class TrackingControls(QWidget):
    """
    The TrackingControlsWidget provides buttons to create tasks, start general work, pause, and end work.
    """

    create_task = pyqtSignal(str, str, name="create_task")
    general_work = pyqtSignal(name="general_work")
    pause = pyqtSignal(name="pause")
    end_of_work = pyqtSignal(name="end_of_work")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QHBoxLayout()
        self.setLayout(layout)

        create_task_btn = QPushButton(text="Create task")
        create_task_btn.clicked.connect(self._clicked_create_task)
        self._general_work_btn = QPushButton(text="General work")
        self._general_work_btn.clicked.connect(self.general_work)
        self._pause_btn = QPushButton(text="Pause", enabled=False)
        self._pause_btn.clicked.connect(self.pause)
        end_of_work_btn = QPushButton(text="End of work")
        end_of_work_btn.clicked.connect(self.end_of_work)

        layout.addWidget(create_task_btn)
        layout.addStretch()
        for widget in (self._general_work_btn, self._pause_btn, end_of_work_btn):
            layout.addWidget(widget)

    def enable_pause_button(self):
        self._pause_btn.setEnabled(True)

    def disable_pause_button(self):
        self._pause_btn.setEnabled(False)

    def enable_general_work_button(self):
        self._general_work_btn.setEnabled(True)

    def disable_general_work_button(self):
        self._general_work_btn.setEnabled(False)

    @pyqtSlot(bool, name="_clicked_create_task")
    @log_exceptions
    def _clicked_create_task(self, b):
        w = CreateTaskDialog(parent=self)
        w.accepted.connect(self.create_task)
        w.show()
