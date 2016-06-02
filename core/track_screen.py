from PyQt5.QtWidgets import QWidget, QLabel


class TrackScreen(QWidget):

    def __init__(self, *args, **kwargs):
        super(TrackScreen, self).__init__(*args, **kwargs)

        self.user = None

        self.lbl = QLabel(text="track screen", parent=self)
