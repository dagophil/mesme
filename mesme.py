import logging
import sys

from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget

from ui.login_screen import LoginScreen
from ui.track_screen import TrackScreen


class MesmeMainWindow(QWidget):
    """
    The main window of mesme.
    """

    def __init__(self, *args, **kwargs):
        super(MesmeMainWindow, self).__init__(*args, **kwargs)

        # Create the main window layout.
        self.setMinimumSize(800, 600)
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        # Create the screens.
        self.screens = {
            "login_screen": LoginScreen(parent=self),
            "track_screen": TrackScreen(parent=self)
        }

        # Add the screens to the layout and connect the screen switch signal.
        for screen in self.screens.values():
            screen.onSwitchScreen.connect(self.onSwitchScreen)
            self.layout.addWidget(screen)

        # Start with the login screen.
        self.onSwitchScreen("login_screen")

    def onSwitchScreen(self, name):
        """
        Switch to the screen with the given name.
        :param name: screen name
        """
        if name not in self.screens:
            logging.warning("Tried to open non-existing screen: " + name)
        else:
            self.layout.setCurrentWidget(self.screens[name])


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
    app = QApplication(sys.argv)
    main_window = MesmeMainWindow()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
