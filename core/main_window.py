from PyQt5.QtWidgets import QWidget, QStackedLayout
from PyQt5.QtCore import pyqtSlot

from .login_screen import LoginScreen
from .track_screen import TrackScreen
from .common import log_exceptions
from .user_profile import UserProfile


class MainWindow(QWidget):
    """
    The main window of mesme. It controls the transitions between screens.
    """

    def __init__(self, *args, **kwargs):
        """
        Create the screens.
        """
        super().__init__(*args, **kwargs)

        # Create the main window layout.
        self.setMinimumSize(800, 600)
        self.setWindowTitle("mesme")
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        # Create the login screen.
        login_screen = LoginScreen()
        login_screen.login_successful.connect(self.on_login)
        self.layout.addWidget(login_screen)
        self.layout.setCurrentWidget(login_screen)

    @pyqtSlot(str, UserProfile, name="on_login")
    @log_exceptions
    def on_login(self, user_display_name, user_profile):
        """
        Switch to the track screen.
        """
        track_screen = TrackScreen(user_display_name, user_profile)
        self.layout.addWidget(track_screen)
        self.layout.setCurrentWidget(track_screen)
