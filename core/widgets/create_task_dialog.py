import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPlainTextEdit

from .ok_cancel_dialog import OkCancelDialog


class CreateTaskDialog(OkCancelDialog):
    """
    Dialog with input fields to create a new task.
    """

    accepted = pyqtSignal(str, str, name="accepted")

    def __init__(self, *args, **kwargs):
        # Add the layout.
        layout = QFormLayout()
        super().__init__("Create a new task", layout, *args, **kwargs)

        # Add the input fields.
        self.input_title = QLineEdit()
        layout.addRow("Title:", self.input_title)
        self.input_description = QPlainTextEdit()
        layout.addRow("Description:", self.input_description)

    def accept(self):
        """
        Accept the dialog if the title is non-empty.
        """
        title = self.input_title.text()
        description = self.input_description.toPlainText()
        if len(title) == 0:
            self.show_error("Title must not be empty.")
        else:
            self.accepted.emit(title, description)
            self.close()
