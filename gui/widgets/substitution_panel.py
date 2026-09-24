from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)


class SubstitutionPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Character", "Replacements"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(180)

        defaults = [
            ("a", "@,4"),
            ("e", "3"),
            ("i", "1,!"),
            ("o", "0"),
            ("s", "$,5"),
            ("t", "7,+"),
        ]

        self.set_rules({char: [part.strip() for part in repl.split(",") if part.strip()] for char, repl in defaults})

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Rule")
        self.remove_btn = QPushButton("Remove Rule")
        self.add_btn.setObjectName("secondaryButton")
        self.remove_btn.setObjectName("secondaryButton")

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.remove_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.add_btn.clicked.connect(self.add_row)
        self.remove_btn.clicked.connect(self.remove_row)

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))

    def remove_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)

    def set_enabled(self, enabled):
        self.table.setEnabled(enabled)
        self.add_btn.setEnabled(enabled)
        self.remove_btn.setEnabled(enabled)

    def set_rules(self, rules):
        self.table.setRowCount(0)
        for char, replacements in (rules or {}).items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(char)))
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(",".join(replacements)),
            )

    def get_rules(self):
        rules = {}

        for row in range(self.table.rowCount()):
            char_item = self.table.item(row, 0)
            repl_item = self.table.item(row, 1)

            if not char_item or not repl_item:
                continue

            char = char_item.text().strip().lower()
            if not char:
                continue

            replacements = [
                part.strip()
                for part in repl_item.text().split(",")
                if part.strip()
            ]
            rules[char] = replacements

        return rules
