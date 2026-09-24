from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QHBoxLayout,
)
from engine.estimator import PasswordEstimator


class DashboardCard(QFrame):

    def __init__(self, title, value):
        super().__init__()
        self.setObjectName("dashboardCard")
        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel(str(value))
        self.value.setObjectName("cardValue")

        layout.addWidget(self.title)
        layout.addWidget(self.value)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title = QLabel("KnightForge")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Local wordlist builder for authorized password testing")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(14)

        self.strings = DashboardCard("Base strings", "0")
        self.numbers = DashboardCard("Numbers", "Off")
        self.symbols = DashboardCard("Symbols", "0")
        self.rules = DashboardCard("Active rules", "0")
        self.substitutions = DashboardCard("Substitutions", "Off")
        self.export = DashboardCard("Last export", "—")

        grid.addWidget(self.strings, 0, 0)
        grid.addWidget(self.numbers, 0, 1)
        grid.addWidget(self.symbols, 0, 2)
        grid.addWidget(self.rules, 1, 0)
        grid.addWidget(self.substitutions, 1, 1)
        grid.addWidget(self.export, 1, 2)
        layout.addLayout(grid)

        estimate_row = QHBoxLayout()
        estimate_row.setSpacing(14)
        self.estimated_passwords = DashboardCard("Estimated passwords", "0")
        self.estimated_size = DashboardCard("Estimated file size", "0 Bytes")
        self.estimated_time = DashboardCard("Estimated generate time", "0 sec")
        estimate_row.addWidget(self.estimated_passwords)
        estimate_row.addWidget(self.estimated_size)
        estimate_row.addWidget(self.estimated_time)
        layout.addLayout(estimate_row)

        self.activity = QLabel(
            "Workflow: Base Data → Rules → Preview → Export to .txt"
        )
        self.activity.setObjectName("mutedLabel")
        self.activity.setWordWrap(True)
        layout.addWidget(self.activity)
        layout.addStretch()

    def update_dashboard(self, app_state):
        settings = app_state.settings
        total = PasswordEstimator.estimate(settings)

        self.strings.value.setText(str(len(settings.base_strings)))
        self.numbers.value.setText("On" if settings.use_numbers else "Off")
        self.symbols.value.setText(str(len(settings.symbols or [])))
        self.substitutions.value.setText(
            "On" if getattr(settings, "use_substitutions", True) else "Off"
        )

        active = sum(
            [
                bool(getattr(settings, "use_substitutions", True)),
                bool(getattr(settings, "use_reverse", False)),
                bool(getattr(settings, "use_duplicate", False)),
                bool(getattr(settings, "combine_bases", False)),
                bool(getattr(settings, "use_common_suffixes", False)),
                bool(getattr(settings, "append_years", False)),
                bool(settings.use_numbers),
                bool(settings.symbols),
            ]
        )
        self.rules.value.setText(str(active))
        self.estimated_passwords.value.setText(f"{total:,}")

        average_password_length = 12
        size = total * (average_password_length + 1)

        if size < 1024:
            text = f"{size} Bytes"
        elif size < 1024 * 1024:
            text = f"{size / 1024:.2f} KB"
        elif size < 1024 * 1024 * 1024:
            text = f"{size / (1024 * 1024):.2f} MB"
        else:
            text = f"{size / (1024 * 1024 * 1024):.2f} GB"

        self.estimated_size.value.setText(text)

        speed = 100000
        seconds = total / speed if speed else 0
        if seconds < 60:
            eta = f"{seconds:.1f} sec"
        elif seconds < 3600:
            eta = f"{seconds / 60:.1f} min"
        else:
            eta = f"{seconds / 3600:.1f} hr"

        self.estimated_time.value.setText(eta)

    def set_last_export(self, filename):
        self.export.value.setText(filename)
