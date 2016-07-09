from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout, QMessageBox, QDialog


class OkCancelDialog(QDialog):
    """
    A dialog with the buttons Ok and Cancel.
    """

    def __init__(self, title, content_layout, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the dialog properties.
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # remove the [?] box

        # Add the layout.
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addLayout(content_layout)

        # Add the dialog buttons.
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def show_error(self, text, title="Error"):
        """
        Show a message box with the given text and title.
        :param text: The text.
        :param title: The title.
        """
        msg = QMessageBox(text=text, parent=self)
        msg.setWindowTitle(title)
        msg.show()
