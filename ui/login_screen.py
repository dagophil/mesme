from PyQt5.QtWidgets import QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

from .screen import Screen


class LoginScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(LoginScreen, self).__init__(*args, **kwargs)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        combo = QComboBox()
        combo.addItem("")
        combo.addItem("Philip")
        self.layout.addWidget(combo)

        btn = QPushButton(text="Login")
        btn.clicked.connect(self.onLogin)
        self.layout.addWidget(btn)

    def onLogin(self):
        self.onSwitchScreen.emit("track_screen")
