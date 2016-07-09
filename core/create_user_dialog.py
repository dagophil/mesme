import logging
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout, QLineEdit

from .common import global_settings
from .widgets import OkCancelDialog


class CreateUserDialog(OkCancelDialog):
    """
    Dialog with input fields to create a new user.
    """

    accepted = pyqtSignal(dict, name="accepted")

    def __init__(self, existing_names, existing_dbs, *args, **kwargs):
        """
        Create the dialog controls.
        :param existing_names: List with the existing user names.
        :param existing_dbs: List with the existing database filenames.
        """
        layout = QFormLayout()
        super().__init__("Create new user", layout, *args, **kwargs)

        self.existing_names = existing_names
        self.existing_dbs = existing_dbs
        self._data = {}  # the dict that is filled with the user input

        # Add the name input.
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Firstname Lastname")
        layout.addRow("Name:", self.input_name)

    @staticmethod
    def _user_id(name):
        """
        Convert the given name to the corresponding user id. Currently the user id equals the name.
        :param name: The name.
        :return: Returns the user id..
        """
        return name

    def accept(self):
        """
        Accept the dialog if the name is non-empty and not already chosen.
        """
        # Fill the data dict with the user input.
        name = self.input_name.text()
        self._data["display_name"] = name
        self._data["database_user_name"] = self._user_id(name)
        self._data["database_location"] = os.path.join(global_settings.database_dir, global_settings.default_database)

        # Check that name and database filename are not in use already.
        if len(name) == 0:
            self.show_error("Name must not be empty.")
        elif name in self.existing_names:
            self.show_error("The chosen name already exists.")
        else:
            self.accepted.emit(self._data)
            self.close()
