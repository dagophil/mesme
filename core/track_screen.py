import logging

from PyQt5.QtWidgets import QWidget, QLabel

from .user_profile import UserProfile
from .database_connector import DatabaseConnector


class TrackScreen(QWidget):

    def __init__(self, user_display_name, user_profile, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert isinstance(user_profile, UserProfile)

        self.user_display_name = user_display_name
        self.user_name = user_profile["database_user_name"]
        self.database = DatabaseConnector(user_profile["database_location"])

        self.lbl = QLabel(text="track screen", parent=self)
