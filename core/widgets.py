import logging

from PyQt5.QtCore import QTime, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFormLayout, QTimeEdit, QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy, \
    QDialog, QDialogButtonBox, QVBoxLayout, QMessageBox

from .common import log_exceptions


class WeekTimeEdit(QFormLayout):
    """
    The WeekTimeEdit is a QWidget input for time (hours, minutes) per week day.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        times = 5*[QTime(8, 0)] + 2*[QTime(0, 0)]

        self._time_inputs = {}

        for day, time in zip(self._days, times):
            time_input = QTimeEdit(time=time)
            self._time_inputs[day] = time_input
            self.addRow(day + ":", time_input)

    def get_time(self, day):
        """
        Returns the input time of the given day. Valid days are "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su".
        :param day: The day.
        :return: Returns the input time.
        """
        if day in self._time_inputs:
            return self._time_inputs[day].time()
        else:
            raise IndexError("Invalid key: " + day)

    def items(self):
        """
        Returns a dict {day: time}, where day is the day ("Mo", "Tu", ...) and time is the corresponding QTime input
        value.
        :return: Returns the {day: time} dict.
        """
        return [(day, self._time_inputs[day].time()) for day in self._days]


class TaskWidget(QWidget):
    """
    The TaskWidget is a QWidget with two labels and three buttons. It is used to show title and description of a task
    and provides signals to start and stop the time tracking for that task.
    """

    start = pyqtSignal(int, name="start")
    stop = pyqtSignal(int, name="stop")
    done = pyqtSignal(int, name="done")

    def __init__(self, task_uid, title, description, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._task_uid = task_uid

        # Create the layout.
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Create the labels and the buttons.
        title = QLabel(text=title)
        description = QLabel(text=description)
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        start_btn = QPushButton(text="Start")
        start_btn.clicked.connect(self._clicked_start)
        stop_btn = QPushButton(text="Stop")
        stop_btn.clicked.connect(self._clicked_stop)
        done_btn = QPushButton(text="Done")
        done_btn.clicked.connect(self._clicked_done)

        for widget in (title, description, start_btn, stop_btn, done_btn):
            layout.addWidget(widget)

    @pyqtSlot(bool, name="clicked_start")
    @log_exceptions
    def _clicked_start(self, b):
        self.start.emit(self._task_uid)

    @pyqtSlot(bool, name="clicked_stop")
    @log_exceptions
    def _clicked_stop(self, b):
        self.stop.emit(self._task_uid)

    @pyqtSlot(bool, name="clicked_done")
    @log_exceptions
    def _clicked_done(self, b):
        self.done.emit(self._task_uid)


class TrackingControlsWidget(QWidget):
    """
    The TrackingControlsWidget provides buttons to create tasks, start general work, pause, and end work.
    """

    create_task = pyqtSignal(name="create_task")
    general_work = pyqtSignal(name="general_work")
    pause = pyqtSignal(name="pause")
    end_of_work = pyqtSignal(name="end_of_work")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self.create_task.emit()

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


class OkCancelDialog(QDialog):
    """
    A dialog with the buttons Ok and Cancel.
    """

    def __init__(self, title, content_layout, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the dialog properties.
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # remove the [?] box

        # Add the layout.
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addLayout(content_layout)

        # Add the dialog buttons.
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def show_error(self, text, title="Error"):
        """
        Show a message box with the given text and title.
        :param text: The text.
        :param title: The title.
        """
        msg = QMessageBox(text=text, parent=self)
        msg.setWindowTitle(title)
        msg.show()
