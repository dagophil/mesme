from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from .ok_cancel_dialog import OkCancelDialog


class DeleteTaskDialog(OkCancelDialog):
    """
    Dialog that asks the user if the task should really be deleted.
    """

    accepted = pyqtSignal(int, name="accepted")

    def __init__(self, task_uid, task_title, *args, **kwargs):
        layout = QVBoxLayout()
        super().__init__("Confirm deletion", layout, *args, **kwargs)

        self.task_uid = task_uid

        question_text = "The task with the title <b>%s</b> will be deleted.\nContinue?" % task_title
        question_lbl = QLabel(text=question_text)
        layout.addWidget(question_lbl)

    def accept(self):
        self.accepted.emit(self.task_uid)
        self.close()
