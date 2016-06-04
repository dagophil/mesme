import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QHBoxLayout, QToolButton, QMessageBox


class CreateUserDialog(QDialog):
    """
    Dialog with input fields to create a new user.
    """

    accepted = pyqtSignal(dict)
    rejected = pyqtSignal()

    def __init__(self, existing_names, *args, **kwargs):
        """
        Create the dialog controls.
        """
        super(CreateUserDialog, self).__init__(*args, **kwargs)

        self.existing_names = existing_names
        self._accepted = False
        self._data = {}

        self.setWindowTitle("Create new user")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # remove the [?] box

        layout = QFormLayout()
        self.setLayout(layout)

        self.input_name = QLineEdit()
        layout.addRow("Name:", self.input_name)

        db_file_layout = QHBoxLayout()
        self.input_db_file = QLineEdit()
        input_db_file_btn = QToolButton(text="...")
        db_file_layout.addWidget(self.input_db_file)
        db_file_layout.addWidget(input_db_file_btn)
        layout.addRow("Database filename:", db_file_layout)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.on_accepted)
        btn_box.rejected.connect(self.on_rejected)
        layout.addWidget(btn_box)

    def _show_error(self, text, title="Error"):
        """
        Show a message box with the given text and title.
        :param text: The text.
        :param title: The title.
        """
        msg = QMessageBox(text=text, parent=self)
        msg.setWindowTitle(title)
        msg.show()

    def on_accepted(self):
        """
        Check if the input is valid. If so, set accepted to true and close the dialog.
        """
        name = self.input_name.text()
        if len(name) == 0:
            self._show_error("Name must not be empty.")
        elif name in self.existing_names:
            self._show_error("The chosen name already exists.")
        else:
            self._accepted = True
            self.close()

    def on_rejected(self):
        """
        Set accepted to false and close the dialog.
        """
        self._accepted = False
        self.close()

    def closeEvent(self, event: QCloseEvent):
        """
        When the dialog is closed, either the accepted or the rejected signal is emitted.
        :param event: The close event.
        """
        if self._accepted:
            self.accepted.emit(self._data)
        else:
            self.rejected.emit()
        event.accept()
