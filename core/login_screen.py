import logging
import os

from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from .user_profile import UserProfileCollection, UserProfile


class LoginScreen(QWidget):
    """
    The login screen lets the user select a user profile or create a new one.
    """

    onLoginSuccessful = pyqtSignal(name="onLogin")

    def __init__(self, *args, **kwargs):
        super(LoginScreen, self).__init__(*args, **kwargs)

        self.user = None

        # Load the user profile collection.
        self.profile_location = UserProfileCollection.default_location()
        self._load_profile_collection()

        # Create and set the widget layout.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Fill the select-user combobox with the loaded profile names.
        self.select_user_combobox = QComboBox()
        layout.addWidget(self.select_user_combobox)
        self.select_user_combobox.addItem("")
        for name, profile in self.user_profile_collection.items():
            assert isinstance(profile, UserProfile)
            self.select_user_combobox.addItem(name)

        btn = QPushButton(text="Login")
        layout.addWidget(btn)
        btn.clicked.connect(self.on_login)

        txt = QLabel(text="<a href='#'>Create new user</a>")
        layout.addWidget(txt)
        txt.setContextMenuPolicy(Qt.PreventContextMenu)
        txt.linkActivated.connect(self.on_create_new_user)

    def _load_profile_collection(self):
        """
        Load the profile collection.
        """
        if os.path.isfile(self.profile_location):
            self.user_profile_collection = UserProfileCollection.from_file(self.profile_location)
        elif not os.path.exists(self.profile_location):
            self.user_profile_collection = UserProfileCollection()
            self.user_profile_collection.save(self.profile_location)
        else:
            raise RuntimeError("Could not create profile collection file.")

    def on_login(self):
        """
        If something is selected in the select-user combobox, the onLoginSuccessful is emitted.
        """
        if self.select_user_combobox.currentIndex() != 0:
            name = self.select_user_combobox.currentText()
            logging.debug("TODO: Do login for user " + name)
        else:
            logging.debug("TODO: Show message that something has to be selected.")

    def on_create_new_user(self):
        """
        Show the dialog to create a new user.
        """
        logging.debug("TODO: Show create-user dialog.")
