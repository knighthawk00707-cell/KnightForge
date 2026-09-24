from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QGroupBox,
)


class PlacementPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("Placement Options")

        group_layout = QVBoxLayout()

        self.prefix = QCheckBox("Prefix")
        self.prefix.setChecked(True)

        self.suffix = QCheckBox("Suffix")
        self.suffix.setChecked(True)

        self.every_position = QCheckBox("Every Position")

        self.before_each = QCheckBox("Before Every Character")

        self.after_each = QCheckBox("After Every Character")

        self.between_each = QCheckBox("Between Every Character")

        self.random_position = QCheckBox("Random Position")

        self.random_position.setToolTip(
            "Places the insert at one random index. Useful for sample lists, not repeatable dumps."
        )

        group_layout.addWidget(self.prefix)
        group_layout.addWidget(self.suffix)
        group_layout.addWidget(self.every_position)
        group_layout.addWidget(self.before_each)
        group_layout.addWidget(self.after_each)
        group_layout.addWidget(self.between_each)
        group_layout.addWidget(self.random_position)

        group.setLayout(group_layout)

        layout.addWidget(group)
        
    def set_settings(self, settings):
        settings = settings or {}
        self.prefix.setChecked(settings.get("prefix", True))
        self.suffix.setChecked(settings.get("suffix", True))
        self.every_position.setChecked(settings.get("every_position", False))
        self.before_each.setChecked(settings.get("before_each", False))
        self.after_each.setChecked(settings.get("after_each", False))
        self.between_each.setChecked(settings.get("between_each", False))
        self.random_position.setChecked(settings.get("random_position", False))

    def get_settings(self):
        return {
        "prefix": self.prefix.isChecked(),
        "suffix": self.suffix.isChecked(),
        "every_position": self.every_position.isChecked(),
        "before_each": self.before_each.isChecked(),
        "after_each": self.after_each.isChecked(),
        "between_each": self.between_each.isChecked(),
        "random_position": self.random_position.isChecked(),
    }