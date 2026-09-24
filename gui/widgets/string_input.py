from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton


class StringInput(QWidget):
    def __init__(self, remove_callback):
        super().__init__()

        layout = QHBoxLayout(self)

        self.text = QLineEdit()
        self.text.setPlaceholderText("Enter base string")

        remove_btn = QPushButton("Remove")
        remove_btn.setFixedWidth(90)
        remove_btn.clicked.connect(lambda: remove_callback(self))

        layout.addWidget(self.text)
        layout.addWidget(remove_btn)