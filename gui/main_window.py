import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QStatusBar,
    QMessageBox,
    QToolBar,
    QApplication,
)

from PySide6.QtGui import QAction, QIcon

from models.app_state import AppState

from gui.widgets.sidebar import Sidebar

from gui.pages.dashboard import DashboardPage
from gui.pages.base_data import BaseDataPage
from gui.pages.rules import RulesPage
from gui.pages.preview import PreviewPage
from gui.pages.export import ExportPage
from gui.pages.settings import SettingsPage


def resource_path(relative_path):
    """
    Return the correct resource path both when running
    from source and when running as a PyInstaller bundle.
    """

    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parents[1]

    return base_path / relative_path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ==========================================
        # Application State
        # ==========================================

        self.app_state = AppState()

        # ==========================================
        # Window
        # ==========================================

        self.setWindowTitle("KnightForge")

        self.setWindowIcon(
            QIcon(
                str(
                    resource_path(
                        "resources/icons/knightforge.png"
                    )
                )
            )
        )

        self.resize(1400, 850)

        self.setStatusBar(QStatusBar())

        # ==========================================
        # Build UI
        # ==========================================

        self.create_central_widget()
        self.create_sidebar()
        self.create_pages()
        self.create_actions()
        self.create_toolbar()
        self.connect_actions()

        # ==========================================
        # Initial State
        # ==========================================

        self.dashboard.update_dashboard(
            self.app_state
        )

        self.pages.setCurrentIndex(0)

        print("MainWindow initialized")

    # ==============================================
    # Central Widget
    # ==============================================

    def create_central_widget(self):

        central = QWidget()

        self.setCentralWidget(central)

        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.layout.setSpacing(0)

        central.setLayout(self.layout)

    # ==============================================
    # Sidebar
    # ==============================================

    def create_sidebar(self):

        self.sidebar = Sidebar()

        self.layout.addWidget(
            self.sidebar
        )

    # ==============================================
    # Pages
    # ==============================================

    def create_pages(self):

        self.pages = QStackedWidget()

        self.dashboard = DashboardPage()

        self.base_data = BaseDataPage(
            self.app_state
        )

        self.rules = RulesPage(
            self.app_state
        )

        self.preview = PreviewPage(
            self.app_state
        )

        self.export = ExportPage(
            self.app_state
        )

        self.settings_page = SettingsPage(
            self.app_state
        )

        self.pages.addWidget(
            self.dashboard
        )

        self.pages.addWidget(
            self.base_data
        )

        self.pages.addWidget(
            self.rules
        )

        self.pages.addWidget(
            self.preview
        )

        self.pages.addWidget(
            self.export
        )

        self.pages.addWidget(
            self.settings_page
        )

        self.layout.addWidget(
            self.pages,
            1,
        )

        print(
            "Pages:",
            self.pages.count(),
        )

    # ==============================================
    # Actions
    # ==============================================

    def create_actions(self):

        self.new_project_action = QAction(
            QIcon.fromTheme("document-new"),
            "New Project",
            self,
        )

        self.open_project_action = QAction(
            QIcon.fromTheme("document-open"),
            "Open Project",
            self,
        )

        self.save_project_action = QAction(
            QIcon.fromTheme("document-save"),
            "Save Project",
            self,
        )

        self.export_action = QAction(
            QIcon.fromTheme("document-export"),
            "Export",
            self,
        )

        self.exit_action = QAction(
            QIcon.fromTheme("application-exit"),
            "Exit",
            self,
        )

        self.clear_preview_action = QAction(
            "Clear Preview",
            self,
        )

        self.about_action = QAction(
            "About KnightForge",
            self,
        )

        # ==========================================
        # Shortcuts
        # ==========================================

        self.new_project_action.setShortcut(
            "Ctrl+N"
        )

        self.open_project_action.setShortcut(
            "Ctrl+O"
        )

        self.save_project_action.setShortcut(
            "Ctrl+S"
        )

        self.export_action.setShortcut(
            "Ctrl+E"
        )

        self.exit_action.setShortcut(
            "Ctrl+Q"
        )

        # ==========================================
        # Status Tips
        # ==========================================

        self.new_project_action.setStatusTip(
            "Create a new project"
        )

        self.open_project_action.setStatusTip(
            "Open an existing project"
        )

        self.save_project_action.setStatusTip(
            "Save current project"
        )

        self.export_action.setStatusTip(
            "Export generated passwords"
        )

        self.exit_action.setStatusTip(
            "Exit KnightForge"
        )

    # ==============================================
    # Toolbar
    # ==============================================

    def create_toolbar(self):

        self.toolbar = QToolBar(
            "Main Toolbar"
        )

        self.toolbar.setMovable(False)

        self.addToolBar(
            self.toolbar
        )

        self.toolbar.addAction(
            self.new_project_action
        )

        self.toolbar.addAction(
            self.open_project_action
        )

        self.toolbar.addAction(
            self.save_project_action
        )

        self.toolbar.addSeparator()

        self.toolbar.addAction(
            self.export_action
        )

        self.toolbar.addSeparator()

        self.toolbar.addAction(
            self.about_action
        )

    # ==============================================
    # Connections
    # ==============================================

    def connect_actions(self):

        self.sidebar.page_changed.connect(
            self.change_page
        )

        self.new_project_action.triggered.connect(
            self.new_project
        )

        self.exit_action.triggered.connect(
            self.close
        )

        self.save_project_action.triggered.connect(
            self.settings_page.save_project_file
        )

        self.open_project_action.triggered.connect(
            self.settings_page.load_project_file
        )

        self.export_action.triggered.connect(
            self.export.export_passwords
        )

        self.clear_preview_action.triggered.connect(
            self.preview.preview_panel.clear
        )

        self.about_action.triggered.connect(
            self.show_about
        )

    # ==============================================
    # New Project
    # ==============================================

    def change_page(self, index):
        self.pages.setCurrentIndex(index)
        self.sidebar.set_active(index)
        if index == 0:
            self.sync_settings()

    def new_project(self):

        from models.settings import GeneratorSettings

        reply = QMessageBox.question(
            self,
            "New Project",
            (
                "Discard the current project "
                "and create a new one?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        self.app_state.settings = (
            GeneratorSettings()
        )

        self.refresh_all_pages()

        if hasattr(
            self.preview,
            "clear_preview",
        ):
            self.preview.clear_preview()

        elif hasattr(
            self.preview,
            "preview_panel",
        ):
            self.preview.preview_panel.clear()

        self.dashboard.update_dashboard(
            self.app_state
        )

        self.statusBar().showMessage(
            "New project created",
            3000,
        )

    # ==============================================
    # Synchronize Settings
    # ==============================================

    def sync_settings(self):

        self.base_data.save_to_state()

        self.rules.save_to_state()

        self.dashboard.update_dashboard(
            self.app_state
        )

    # ==============================================
    # Refresh Pages
    # ==============================================

    def refresh_all_pages(self):

        if hasattr(
            self.base_data,
            "load_from_state",
        ):
            self.base_data.load_from_state()

        if hasattr(
            self.rules,
            "load_from_state",
        ):
            self.rules.load_from_state()

        self.dashboard.update_dashboard(
            self.app_state
        )

    # ==============================================
    # About
    # ==============================================

    def show_about(self):

        QMessageBox.about(
            self,
            "About KnightForge",
            (
                "KnightForge\n\n"
                "Professional Password "
                "Wordlist Generator\n\n"
                "Version 1.0"
            ),
        )

    # ==============================================
    # Close Event
    # ==============================================

    def closeEvent(self, event):

        try:
            self.sync_settings()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Save Error",
                (
                    "Unable to save project "
                    "settings before closing:\n\n"
                    f"{exc}"
                ),
            )

            event.ignore()
            return

        event.accept()

    # ==============================================
    # Show Event
    # ==============================================

    def showEvent(self, event):

        super().showEvent(event)

        self.dashboard.update_dashboard(
            self.app_state
        )
