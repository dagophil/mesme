import logging
import os
import string

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTime
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QMessageBox, QLabel, QTimeEdit, QToolTip

from .common import global_settings, log_exceptions


class CreateUserDialog(QDialog):
    """
    Dialog with input fields to create a new user.
    """

    accepted = pyqtSignal(dict, name="accepted")
    rejected = pyqtSignal(name="rejected")

    def __init__(self, existing_names, existing_dbs, *args, **kwargs):
        """
        Create the dialog controls.
        :param existing_names: List with the existing user names.
        :param existing_dbs: List with the existing database filenames.
        """
        super(CreateUserDialog, self).__init__(*args, **kwargs)

        self.existing_names = existing_names
        self.existing_dbs = existing_dbs
        self._accepted = False  # whether the user accepted the dialog by pressing ok
        self._data = {}  # the dict that is filled with the user input

        # Set the dialog properties.
        self.setWindowTitle("Create new user")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # remove the [?] box

        # Create and set the form layout.
        layout = QFormLayout()
        self.setLayout(layout)

        # Add the name input.
        input_name = QLineEdit()
        input_name.setPlaceholderText("Firstname Lastname")
        input_name.textChanged.connect(self._on_input_name_changed)
        layout.addRow("Name:", input_name)

        # Add the database filename input.
        self.input_db_lbl = QLabel(text=self._get_input_db_filename(""))
        self.input_db_lbl.setCursor(Qt.WhatsThisCursor)
        self.input_db_lbl.setToolTip("All databases are stored in " + global_settings.database_dir)
        layout.addRow("Database filename:", self.input_db_lbl)

        # Add the work time inputs.
        time_layout = QFormLayout()
        self.input_work = {}
        for workday in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            self.input_work[workday] = QTimeEdit()
            if workday not in ["Sa", "Su"]:
                self.input_work[workday].setTime(QTime(8, 0))
            time_layout.addRow(workday + ":", self.input_work[workday])
        layout.addRow("Work time:", time_layout)

        # Add the dialog buttons.
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self._on_accepted)
        btn_box.rejected.connect(self._on_rejected)
        layout.addWidget(btn_box)

    @staticmethod
    def _clean_filename(name):
        """
        Remove invalid characters from the given name, such that it can be used as a filename.
        The filename may still be invalid, e. g. if it starts with '.' or '..'.
        :param name: The name.
        :return: The filename.
        """
        valid_chars = "-_. " + string.ascii_letters + string.digits
        name = ''.join(c for c in name if c in valid_chars).strip().lower().replace(" ", "_")
        return name

    def _get_input_db_filename(self, name):
        """
        Convert the given name to the database filename.
        :return: The database filename.
        """
        name = self._clean_filename(name)
        if len(name) == 0:
            name = "mesme_firstname_lastname.db"
        else:
            name = "mesme_" + name + ".db"
        return name

    @pyqtSlot(str, name="_on_input_name_changed")
    @log_exceptions
    def _on_input_name_changed(self, name):
        """
        Update the database filename if no custom database name was chosen.
        :param name: The user name.
        """
        self._data["name"] = name
        db_filename = self._get_input_db_filename(name)
        self.input_db_lbl.setText(db_filename)
        full_filename = os.path.join(global_settings.database_dir, db_filename)
        self._data["database_location"] = full_filename

    def _show_error(self, text, title="Error"):
        """
        Show a message box with the given text and title.
        :param text: The text.
        :param title: The title.
        """
        msg = QMessageBox(text=text, parent=self)
        msg.setWindowTitle(title)
        msg.show()

    @pyqtSlot(name="_on_accepted")
    @log_exceptions
    def _on_accepted(self):
        """
        Check if the input is valid. If so, set accepted to true and close the dialog.
        """
        # Write the work time into the data array.
        worktime = {}
        for workday, input_widget in self.input_work.items():
            time = input_widget.time()
            worktime[workday] = (time.hour(), time.minute())
        self._data["worktime"] = worktime

        # Check that name and database filename are not in use already.
        name = self._data.get("name", "")
        database_location = self._data.get("database_location", "")
        if len(name) == 0:
            self._show_error("Name must not be empty.")
        elif name in self.existing_names:
            self._show_error("The chosen name already exists.")
        elif database_location in self.existing_dbs:
            self._show_error("The chosen database already exists.")
        else:
            self._accepted = True
            self.close()

    @pyqtSlot(name="_on_rejected")
    @log_exceptions
    def _on_rejected(self):
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
