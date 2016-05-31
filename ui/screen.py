from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class Screen(QWidget):

    onSwitchScreen = pyqtSignal(str, name="onSwitchScreen")

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
