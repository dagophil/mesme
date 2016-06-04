from PyQt5.QtWidgets import QWidget, QStackedLayout
from PyQt5.QtCore import pyqtSlot

from .login_screen import LoginScreen
from .track_screen import TrackScreen
from .common import log_exceptions


class MainWindow(QWidget):
    """
    The main window of mesme. It controls the transitions between screens.
    """

    def __init__(self, *args, **kwargs):
        """
        Create the screens.
        """
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the main window layout.
        self.setMinimumSize(800, 600)
        self.setWindowTitle("mesme")
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        # Create the login screen.
        self.login_screen = LoginScreen()
        self.login_screen.login_successful.connect(self.on_login)
        self.layout.addWidget(self.login_screen)

        # Create the track screen.
        self.track_screen = TrackScreen()
        self.layout.addWidget(self.track_screen)

        # Activate the login screen.
        self.layout.setCurrentWidget(self.login_screen)

    @pyqtSlot(name="on_login")
    @log_exceptions
    def on_login(self):
        """
        Switch to the track screen.
        """
        self.track_screen.user = self.login_screen.user
        self.layout.setCurrentWidget(self.track_screen)
