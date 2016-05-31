from PyQt5.QtWidgets import QWidget, QLabel

from .screen import Screen


class TrackScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(TrackScreen, self).__init__(*args, **kwargs)

        self.lbl = QLabel(text="track screen", parent=self)
