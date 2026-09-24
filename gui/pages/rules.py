from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QCheckBox,
    QComboBox,
    QSpinBox,
    QScrollArea,
    QFormLayout,
)

from gui.widgets.substitution_panel import SubstitutionPanel
from gui.widgets.placement_panel import PlacementPanel
from models.settings import DEFAULT_SUBSTITUTION_RULES


class RulesPage(QWidget):

    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(16)

        title = QLabel("Rules")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Turn combination styles on or off. Smaller, targeted rules "
            "build a tighter wordlist for a .txt dump."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)

        page_layout.addWidget(title)
        page_layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(16)

        # Case
        case_group = QGroupBox("Case variations")
        case_layout = QVBoxLayout()
        self.lowercase = QCheckBox("lowercase")
        self.uppercase = QCheckBox("UPPERCASE")
        self.capitalize = QCheckBox("Capitalize")
        self.alternate = QCheckBox("aLtErNaTe case")
        self.lowercase.setChecked(True)
        self.capitalize.setChecked(True)
        for box in (self.lowercase, self.uppercase, self.capitalize, self.alternate):
            case_layout.addWidget(box)
        case_group.setLayout(case_layout)
        layout.addWidget(case_group)

        # Substitutions
        substitution_group = QGroupBox("Substitution rules")
        substitution_layout = QVBoxLayout()

        self.use_substitutions = QCheckBox("Enable character substitutions (leet)")
        self.use_substitutions.setChecked(True)
        self.use_substitutions.setToolTip(
            "When off, base strings keep their original characters."
        )
        substitution_layout.addWidget(self.use_substitutions)

        mode_row = QHBoxLayout()
        mode_label = QLabel("Combination style")
        self.substitution_mode = QComboBox()
        self.substitution_mode.addItem("One character at a time (smaller list)", "single")
        self.substitution_mode.addItem("All combinations (larger list)", "all")
        mode_row.addWidget(mode_label)
        mode_row.addWidget(self.substitution_mode, 1)
        substitution_layout.addLayout(mode_row)

        self.substitution_panel = SubstitutionPanel()
        substitution_layout.addWidget(self.substitution_panel)
        substitution_group.setLayout(substitution_layout)
        layout.addWidget(substitution_group)

        self.use_substitutions.toggled.connect(self._toggle_substitutions)
        self._toggle_substitutions(True)

        # Extra transforms
        extra_group = QGroupBox("Wordlist extras")
        extra_layout = QVBoxLayout()
        self.use_reverse = QCheckBox("Add reversed strings")
        self.use_duplicate = QCheckBox("Add doubled strings (wordword)")
        self.combine_bases = QCheckBox("Combine base strings with each other")
        self.use_common_suffixes = QCheckBox(
            "Add common suffixes (123, 1234, 111, 007…)"
        )
        extra_layout.addWidget(self.use_reverse)
        extra_layout.addWidget(self.use_duplicate)
        extra_layout.addWidget(self.combine_bases)
        extra_layout.addWidget(self.use_common_suffixes)
        extra_group.setLayout(extra_layout)
        layout.addWidget(extra_group)

        # Years
        year_group = QGroupBox("Years")
        year_layout = QFormLayout()
        self.append_years = QCheckBox("Append / prefix years from the range below")
        self.year_from = QSpinBox()
        self.year_to = QSpinBox()
        for box in (self.year_from, self.year_to):
            box.setRange(1900, 2100)
        self.year_from.setValue(1990)
        self.year_to.setValue(2026)
        year_layout.addRow(self.append_years)
        year_layout.addRow("From", self.year_from)
        year_layout.addRow("To", self.year_to)
        year_group.setLayout(year_layout)
        layout.addWidget(year_group)

        # Length filter
        length_group = QGroupBox("Password length filter")
        length_layout = QFormLayout()
        self.min_password_length = QSpinBox()
        self.max_password_length = QSpinBox()
        self.min_password_length.setRange(0, 128)
        self.max_password_length.setRange(0, 128)
        self.min_password_length.setSpecialValueText("No minimum")
        self.max_password_length.setSpecialValueText("No maximum")
        length_layout.addRow("Minimum length", self.min_password_length)
        length_layout.addRow("Maximum length", self.max_password_length)
        hint = QLabel("0 means no limit. Applied after all combination rules.")
        hint.setObjectName("mutedLabel")
        hint.setWordWrap(True)
        length_layout.addRow(hint)
        length_group.setLayout(length_layout)
        layout.addWidget(length_group)

        # Placement
        self.placement_panel = PlacementPanel()
        layout.addWidget(self.placement_panel)

        output_group = QGroupBox("Output hygiene")
        output_layout = QVBoxLayout()
        self.remove_duplicates = QCheckBox("Remove duplicates")
        self.sort_results = QCheckBox("Sort exported .txt file")
        self.remove_duplicates.setChecked(True)
        output_layout.addWidget(self.remove_duplicates)
        output_layout.addWidget(self.sort_results)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        layout.addStretch()
        scroll.setWidget(content)
        page_layout.addWidget(scroll)

    def _toggle_substitutions(self, enabled):
        self.substitution_panel.set_enabled(enabled)
        self.substitution_mode.setEnabled(enabled)

    def save_to_state(self):
        settings = self.app_state.settings

        settings.case_lowercase = self.lowercase.isChecked()
        settings.case_uppercase = self.uppercase.isChecked()
        settings.case_capitalize = self.capitalize.isChecked()
        settings.case_alternate = self.alternate.isChecked()
        settings.use_case = any(
            (
                settings.case_lowercase,
                settings.case_uppercase,
                settings.case_capitalize,
                settings.case_alternate,
            )
        )

        settings.use_substitutions = self.use_substitutions.isChecked()
        settings.substitution_mode = self.substitution_mode.currentData() or "single"
        settings.substitution_rules = self.substitution_panel.get_rules()

        settings.use_reverse = self.use_reverse.isChecked()
        settings.use_duplicate = self.use_duplicate.isChecked()
        settings.combine_bases = self.combine_bases.isChecked()
        settings.use_common_suffixes = self.use_common_suffixes.isChecked()
        settings.append_years = self.append_years.isChecked()
        settings.year_from = self.year_from.value()
        settings.year_to = self.year_to.value()
        settings.min_password_length = self.min_password_length.value()
        settings.max_password_length = self.max_password_length.value()
        settings.placement = self.placement_panel.get_settings()
        settings.remove_duplicates = self.remove_duplicates.isChecked()
        settings.sort_results = self.sort_results.isChecked()

    def load_from_state(self):
        settings = self.app_state.settings

        self.lowercase.setChecked(getattr(settings, "case_lowercase", True))
        self.uppercase.setChecked(getattr(settings, "case_uppercase", False))
        self.capitalize.setChecked(getattr(settings, "case_capitalize", True))
        self.alternate.setChecked(getattr(settings, "case_alternate", False))

        enabled = getattr(settings, "use_substitutions", True)
        self.use_substitutions.setChecked(enabled)
        index = self.substitution_mode.findData(
            getattr(settings, "substitution_mode", "single")
        )
        if index >= 0:
            self.substitution_mode.setCurrentIndex(index)

        rules = settings.substitution_rules or DEFAULT_SUBSTITUTION_RULES
        self.substitution_panel.set_rules(rules)
        self._toggle_substitutions(enabled)

        self.use_reverse.setChecked(getattr(settings, "use_reverse", False))
        self.use_duplicate.setChecked(getattr(settings, "use_duplicate", False))
        self.combine_bases.setChecked(getattr(settings, "combine_bases", False))
        self.use_common_suffixes.setChecked(
            getattr(settings, "use_common_suffixes", False)
        )
        self.append_years.setChecked(getattr(settings, "append_years", False))
        self.year_from.setValue(getattr(settings, "year_from", 1990))
        self.year_to.setValue(getattr(settings, "year_to", 2026))
        self.min_password_length.setValue(getattr(settings, "min_password_length", 0))
        self.max_password_length.setValue(getattr(settings, "max_password_length", 0))
        self.placement_panel.set_settings(settings.placement)
        self.remove_duplicates.setChecked(getattr(settings, "remove_duplicates", True))
        self.sort_results.setChecked(getattr(settings, "sort_results", False))
