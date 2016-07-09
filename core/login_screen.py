import logging

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QLabel

from .common import global_settings, log_exceptions
from .user_profile import UserProfileCollection, UserProfile
from .widgets import CreateUserDialog


class LoginScreen(QWidget):
    """
    The login screen lets the user select a user profile or create a new one.
    """

    login_successful = pyqtSignal(str, UserProfile, name="login_successful")

    def __init__(self, *args, **kwargs):
        """
        Load the user profiles and create the login controls.
        """
        super().__init__(*args, **kwargs)

        # Load the user profile collection.
        try:
            self.user_profile_collection = UserProfileCollection.from_dict(global_settings["users"])
        except KeyError:
            self.user_profile_collection = UserProfileCollection()

        # Create and set the widget layout.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Fill the select-user combobox with the loaded profile names.
        self.select_user_combobox = QComboBox()
        layout.addWidget(self.select_user_combobox)
        self.select_user_combobox.addItem("")
        names = self.user_profile_collection.names()
        names = [(name.lower(), name) for name in names]  # convert to lower case for sorting
        for _, name in sorted(names):
            self.select_user_combobox.addItem(name)

        # Add the login button.
        self.login_btn = QPushButton(text="Login", enabled=False)
        layout.addWidget(self.login_btn)

        # Add the create-user link.
        txt = QLabel(text="<a href='#'>Create new user</a>")
        layout.addWidget(txt)
        txt.setContextMenuPolicy(Qt.PreventContextMenu)

        # Connect signals and slots. This must be done after initializing all class members.
        self.select_user_combobox.currentIndexChanged.connect(self.on_selection_changed)
        self.login_btn.clicked.connect(self.on_login)
        txt.linkActivated.connect(self.on_show_create_user_dialog)

    @pyqtSlot(int, name="on_selection_changed")
    @log_exceptions
    def on_selection_changed(self, i):
        """
        Disable the login button if no username is selected, enable it otherwise.
        :param i: The current selected index in the selection combobox.
        """
        self.login_btn.setEnabled(i != 0)

    @pyqtSlot(name="on_login")
    @log_exceptions
    def on_login(self):
        """
        If something is selected in the select-user combobox, the login_successful is emitted.
        """
        if self.select_user_combobox.currentIndex() != 0:
            name = self.select_user_combobox.currentText()
            profile = self.user_profile_collection[name]
            self.login_successful.emit(name, profile)
        else:
            logging.warning("LoginScreen.on_login(): Tried to login without selecting a user.")

    @pyqtSlot(name="on_show_create_user_dialog")
    @log_exceptions
    def on_show_create_user_dialog(self):
        """
        Show the dialog to create a new user.
        """
        names = self.user_profile_collection.names()
        db_locations = self.user_profile_collection.db_locations()
        w = CreateUserDialog(names, db_locations, parent=self)
        w.setAttribute(Qt.WA_DeleteOnClose, True)
        w.accepted.connect(self.on_create_user)
        w.show()

    @pyqtSlot(dict, name="on_create_user")
    @log_exceptions
    def on_create_user(self, data):
        """
        Add the user to the profile collection.
        """
        try:
            name = data.pop("display_name")

            profile = UserProfile()
            for key, value in data.items():
                profile[key] = value

            # Add the profile to the collection.
            self.user_profile_collection[name] = profile

            # Add the new name to the combobox while keeping the alphabetical order.
            for i in range(self.select_user_combobox.count()):
                if name.lower() < self.select_user_combobox.itemText(i).lower():
                    self.select_user_combobox.insertItem(i, name)
                    break
            else:
                self.select_user_combobox.addItem(name)
            self.select_user_combobox.setCurrentText(name)

            # Save the created user.
            global_settings["users"] = self.user_profile_collection

        except (KeyError, IndexError, OSError) as ex:
            logging.warning(str(ex))
