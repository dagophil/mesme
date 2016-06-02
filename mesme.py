import logging
import sys

from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget

from core.login_screen import LoginScreen
from core.track_screen import TrackScreen


app = None  # the global QApplication object


class MesmeMainWindow(QWidget):
    """
    The main window of mesme. It controls the transitions between screens.
    """

    def __init__(self, *args, **kwargs):
        super(MesmeMainWindow, self).__init__(*args, **kwargs)

        # Create the main window layout.
        self.setMinimumSize(800, 600)
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        # Create the login screen.
        self.login_screen = LoginScreen()
        self.login_screen.onLoginSuccessful.connect(self.onLogin)
        self.layout.addWidget(self.login_screen)

        # Create the track screen.
        self.track_screen = TrackScreen()
        self.layout.addWidget(self.track_screen)

        # Activate the login screen.
        self.layout.setCurrentWidget(self.login_screen)

    def onLogin(self):
        """
        Switch to the track screen.
        """
        self.track_screen.user = self.login_screen.user
        self.layout.setCurrentWidget(self.track_screen)


def main():
    """
    Create and show the mesme main window.
    :return: return code of the QApplication.
    """
    # Initialize the logger.
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG)

    # Open the main window.
    global app
    app = QApplication(sys.argv)
    main_window = MesmeMainWindow()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
