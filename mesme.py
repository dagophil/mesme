import logging
import sys

from PyQt5.QtWidgets import QApplication

from core.main_window import MainWindow


# The global QApplication object
app = None


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
    main_window = MainWindow()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
