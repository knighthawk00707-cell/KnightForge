from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QApplication,
    QLineEdit,
)

class PreviewPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.search = QLineEdit()
        self.search.setPlaceholderText(
        "Search passwords..."
        )

        layout.addWidget(self.search)
        self.list = QListWidget()

        layout.addWidget(self.list)

        buttons = QHBoxLayout()
        
        self.search.textChanged.connect(
        self.filter_passwords
        )
        
        self.clear_btn = QPushButton("Clear")
        self.copy_btn = QPushButton("Copy Selected")

        buttons.addWidget(self.clear_btn)
        buttons.addWidget(self.copy_btn)

        layout.addLayout(buttons)

        self.clear_btn.clicked.connect(self.clear)
        self.copy_btn.clicked.connect(self.copy_selected)
        
        self.match_label = QLabel("Matches : 0")
        layout.addWidget(self.match_label)
        
        from PySide6.QtWidgets import QAbstractItemView

        self.list.setSelectionMode(
    QAbstractItemView.ExtendedSelection
    )

    def add_password(self, password):
        self.list.addItem(password)

    def clear(self):
        self.list.clear()

    def count(self):
        return self.list.count()

    def copy_selected(self):
        items = self.list.selectedItems()

        if not items:
            return

        text: str = "\n".join(
            item.text() for item in items
        )

        QApplication.clipboard().setText(text)
    
    def filter_passwords(self, text):
        text = text.lower()
        matches = 0

        for row in range(self.list.count()):
            item = self.list.currentItem()
            visible = text in item.text().lower()
            item.setHidden(not visible)

            if visible:
                matches += 1

        self.match_label.setText(f"Matches : {matches}")