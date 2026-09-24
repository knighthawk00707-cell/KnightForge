from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QProgressBar,
)

from PySide6.QtCore import QThread

from gui.widgets.preview_panel import PreviewPanel
from workers.generation_worker import GenerationWorker


class PreviewPage(QWidget):

    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state

        self.thread = None
        self.worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Preview")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Generate a sample of the wordlist. Export writes the full list to .txt."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ==========================
        # Buttons
        # ==========================

        button_layout = QHBoxLayout()

        self.generate_btn = QPushButton("Generate sample")
        self.generate_btn.setObjectName("primaryButton")
        self.pause_btn = QPushButton("Pause")
        self.resume_btn = QPushButton("Resume")
        self.cancel_btn = QPushButton("Cancel")
        self.pause_btn.setObjectName("secondaryButton")
        self.resume_btn.setObjectName("secondaryButton")
        self.cancel_btn.setObjectName("secondaryButton")

        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.resume_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        # ==========================
        # Progress
        # ==========================

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()

        layout.addWidget(self.progress)

        # ==========================
        # Preview
        # ==========================

        preview_group = QGroupBox("Sample wordlist")

        preview_layout = QVBoxLayout()

        self.preview_panel = PreviewPanel()

        preview_layout.addWidget(self.preview_panel)

        preview_group.setLayout(preview_layout)

        layout.addWidget(preview_group)

        # ==========================
        # Statistics
        # ==========================

        stats = QGroupBox("Statistics")

        stats_layout = QVBoxLayout()

        self.generated = QLabel("Generated : 0")
        self.speed = QLabel("Speed : 0 passwords/sec")
        self.elapsed = QLabel("Elapsed : 00:00:00")

        stats_layout.addWidget(self.generated)
        stats_layout.addWidget(self.speed)
        stats_layout.addWidget(self.elapsed)

        stats.setLayout(stats_layout)

        layout.addWidget(stats)

        # ==========================
        # Signals
        # ==========================

        self.generate_btn.clicked.connect(self.generate_passwords)
        self.pause_btn.clicked.connect(self.pause_generation)
        self.resume_btn.clicked.connect(self.resume_generation)
        self.cancel_btn.clicked.connect(self.cancel_generation)

    # ==================================================

    def generate_passwords(self):

        if self.thread is not None:
            return

        window = self.window()

        if hasattr(window, "sync_settings"):
            window.sync_settings()

        self.preview_panel.clear()

        self.generated.setText("Generated : 0")
        self.speed.setText("Speed : 0 passwords/sec")
        self.elapsed.setText("Elapsed : 00:00:00")

        self.progress.show()

        self.generate_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        self.thread = QThread()
        self.worker = GenerationWorker(self.app_state.settings)

        self.worker.moveToThread(self.thread)

        # Worker starts
        self.thread.started.connect(self.worker.run)

        # Worker signals
        self.worker.password_generated.connect(self.add_password)
        self.worker.progress.connect(self.update_progress)
        self.worker.speed.connect(self.update_speed)
        self.worker.elapsed.connect(self.update_elapsed)

        # Finish sequence
        self.worker.finished.connect(self.generation_finished)
        self.worker.finished.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.cleanup_thread)

        self.thread.start()

    # ==================================================

    def cleanup_thread(self):

        self.worker = None
        self.thread = None

    # ==================================================

    def add_password(self, password):

        self.preview_panel.add_password(password)

    # ==================================================

    def update_progress(self, count):

        self.generated.setText(
            f"Generated : {count}"
        )

    # ==================================================

    def update_speed(self, speed):

        self.speed.setText(
            f"Speed : {speed:.0f} passwords/sec"
        )

    # ==================================================

    def update_elapsed(self, seconds):

        seconds = int(seconds)

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        self.elapsed.setText(
            f"Elapsed : {h:02}:{m:02}:{s:02}"
        )

    # ==================================================

    def generation_finished(self):

        self.progress.hide()

        self.generate_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

    # ==================================================

    def pause_generation(self):

        if self.worker:
            self.worker.pause()
            self.pause_btn.setEnabled(False)
            self.resume_btn.setEnabled(True)

    # ==================================================

    def resume_generation(self):

        if self.worker:
            self.worker.resume()
            self.pause_btn.setEnabled(True)
            self.resume_btn.setEnabled(False)

    # ==================================================

    def cancel_generation(self):

        if self.worker:
            self.worker.stop()