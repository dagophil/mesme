import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication, QStyleFactory

from core.main_window import MainWindow


# The global QApplication object
app = None


# Create the argument parser.
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--style_name", type=str, default=None)


def initialize_logging():
    """
    Set the logging level and the logging format.
    """
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG)


def set_application_style(qapp, style_name):
    """
    Check that style_name is in the list of available styles and set the application style.
    :param qapp: The QApplication.
    :param style_name: The style name.
    """
    styles = QStyleFactory.keys()
    if style_name is not None:
        if style_name in styles:
            style = QStyleFactory.create(style_name)
            qapp.setStyle(style)
        else:
            logging.info("Style name '%s' is not in list of available styles: %s" % (style_name, str(styles)))


def main(args):
    """
    Create and show the mesme main window.
    :return: Return code of the QApplication.
    """
    global app

    initialize_logging()
    app = QApplication(sys.argv)
    set_application_style(app, args.style_name)
    main_window = MainWindow()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main(parser.parse_args()))
