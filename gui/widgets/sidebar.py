from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal


class Sidebar(QWidget):
    page_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(232)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(8)
        self.setLayout(layout)

        brand = QLabel("KnightForge")
        brand.setObjectName("sidebarBrand")
        tag = QLabel("Wordlist builder")
        tag.setObjectName("sidebarTag")
        layout.addWidget(brand)
        layout.addWidget(tag)
        layout.addSpacing(12)

        pages = [
            "Dashboard",
            "Base Data",
            "Rules",
            "Preview",
            "Export",
            "Settings",
        ]

        self.buttons = []
        for index, page in enumerate(pages):
            button = QPushButton(page)
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.setMinimumHeight(44)
            button.clicked.connect(
                lambda checked=False, i=index: self.page_changed.emit(i)
            )
            layout.addWidget(button)
            self.buttons.append(button)

        layout.addStretch()
        self.set_active(0)

    def set_active(self, index):
        for i, button in enumerate(self.buttons):
            button.setChecked(i == index)
