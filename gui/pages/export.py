from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLineEdit,
    QCheckBox,
    QGroupBox,
)

from controllers.generator_controller import GeneratorController


class ExportPage(QWidget):

    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Export")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Write the generated wordlist to a local .txt file. "
            "Use only on systems you are authorized to test."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        file_group = QGroupBox("Output file")
        file_layout = QVBoxLayout()
        row = QHBoxLayout()
        self.path = QLineEdit()
        self.path.setPlaceholderText("wordlist.txt")
        browse = QPushButton("Browse")
        browse.setObjectName("secondaryButton")
        browse.clicked.connect(self.choose_file)
        row.addWidget(self.path)
        row.addWidget(browse)
        file_layout.addLayout(row)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        options = QGroupBox("Export options")
        options_layout = QVBoxLayout()
        self.unique = QCheckBox("Remove duplicates")
        self.sort = QCheckBox("Sort the file")
        self.unique.setChecked(True)
        options_layout.addWidget(self.unique)
        options_layout.addWidget(self.sort)
        options.setLayout(options_layout)
        layout.addWidget(options)

        self.export_btn = QPushButton("Export wordlist")
        self.export_btn.setObjectName("primaryButton")
        self.export_btn.clicked.connect(self.export_passwords)
        layout.addWidget(self.export_btn)

        self.status = QLabel("Ready")
        self.status.setObjectName("mutedLabel")
        layout.addWidget(self.status)
        layout.addStretch()

    def choose_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export wordlist",
            "wordlist.txt",
            "Text Files (*.txt)",
        )
        if filename:
            self.path.setText(filename)

    def export_passwords(self):
        filename = self.path.text().strip()
        if not filename:
            self.status.setText("Choose a file first.")
            return

        window = self.window()
        if hasattr(window, "sync_settings"):
            window.sync_settings()

        self.app_state.settings.remove_duplicates = self.unique.isChecked()
        self.app_state.settings.sort_results = self.sort.isChecked()

        total = GeneratorController.export(
            self.app_state.settings,
            filename,
        )

        self.status.setText(f"Exported {total:,} lines to {filename}")

        if hasattr(window, "dashboard") and hasattr(window.dashboard, "set_last_export"):
            window.dashboard.set_last_export(filename.split("/")[-1])
