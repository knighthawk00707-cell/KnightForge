from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from controllers.project_controller import ProjectController
from controllers.profiles_controller import ProfileController


class SettingsPage(QWidget):

    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Theme, project files, and generation profiles.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ==========================================
        # Appearance
        # ==========================================

        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()

        self.theme = QComboBox()
        self.theme.addItems([
            "Dark",
            "Light",
        ])

        appearance_layout.addWidget(self.theme)
        appearance_group.setLayout(appearance_layout)
        self.theme.currentTextChanged.connect(self.apply_theme)

        layout.addWidget(appearance_group)

        # ==========================================
        # Performance
        # ==========================================

        performance_group = QGroupBox("Performance")
        performance_layout = QVBoxLayout()

        self.multithreading = QCheckBox(
            "Enable Multi-threading"
        )

        self.autosave = QCheckBox(
            "Auto Save Project"
        )

        performance_layout.addWidget(
            self.multithreading
        )

        performance_layout.addWidget(
            self.autosave
        )

        performance_group.setLayout(
            performance_layout
        )

        layout.addWidget(performance_group)

        # ==========================================
        # Profiles
        # ==========================================

        profile_group = QGroupBox("Generation Profile")
        profile_layout = QVBoxLayout()

        self.profile_combo = QComboBox()

        self.profile_combo.addItems(
            ProfileController.list_profiles()
        )

        profile_layout.addWidget(
            self.profile_combo
        )

        profile_group.setLayout(
            profile_layout
        )

        layout.addWidget(profile_group)

        # ==========================================
        # Project
        # ==========================================

        project_group = QGroupBox("Project")
        project_layout = QVBoxLayout()

        self.save_project_btn = QPushButton(
            "Save Project"
        )

        self.load_project_btn = QPushButton(
            "Load Project"
        )

        project_layout.addWidget(
            self.save_project_btn
        )

        project_layout.addWidget(
            self.load_project_btn
        )

        project_group.setLayout(
            project_layout
        )

        layout.addWidget(project_group)

        self.save_project_btn.clicked.connect(
            self.save_project_file
        )

        self.load_project_btn.clicked.connect(
            self.load_project_file
        )

        # ==========================================
        # About
        # ==========================================

        about = QLabel(
            "KnightForge v1.0\n\n"
            "Professional Password Wordlist Generator\n\n"
            "Developed by Parth Katkar\n"
        )

        layout.addWidget(about)

        layout.addStretch()

    def apply_theme(self, name):
        window = self.window()
        if hasattr(window, "apply_theme"):
            window.apply_theme(name)

    # ==========================================
    # Save Project
    # ==========================================

    def save_project_file(self):

        window = self.window()

        if hasattr(window, "sync_settings"):
            window.sync_settings()

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "KnightForge Project (*.kfproj)",
        )

        if not filename:
            return

        ProjectController.save(
            self.app_state.settings,
            filename,
        )

        QMessageBox.information(
            self,
            "Project Saved",
            "Project saved successfully.",
        )

    # ==========================================
    # Load Project
    # ==========================================

    def load_project_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Project",
            "",
            "KnightForge Project (*.kfproj)",
        )

        if not filename:
            return

        self.app_state.settings = ProjectController.load(
            filename
        )

        window = self.window()

        if hasattr(window, "refresh_all_pages"):
            window.refresh_all_pages()

        QMessageBox.information(
            self,
            "Project Loaded",
            "Project loaded successfully.",
        )