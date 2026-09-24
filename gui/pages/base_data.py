from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QPushButton,
    QScrollArea,
)

from gui.widgets.number_panel import NumberPanel
from gui.widgets.symbol_panel import SymbolPanel
from gui.widgets.string_input import StringInput


class BaseDataPage(QWidget):

    def __init__(self, app_state):
        super().__init__()

        self.app_state = app_state
        self.string_widgets = []

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(16)

        title = QLabel("Base Data")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Names, words, and tokens you already know. Rules on the next "
            "page expand these into the wordlist."
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

        string_group = QGroupBox("Base strings")
        self.string_layout = QVBoxLayout()
        string_group.setLayout(self.string_layout)

        add_row = QHBoxLayout()
        self.add_string_btn = QPushButton("Add string")
        self.add_string_btn.setObjectName("primaryButton")
        self.add_string_btn.clicked.connect(self.add_string)
        add_row.addWidget(self.add_string_btn)
        add_row.addStretch()
        self.string_layout.addLayout(add_row)

        layout.addWidget(string_group)
        self.add_string()

        self.number_panel = NumberPanel()
        number_group = QGroupBox("Numbers")
        number_layout = QVBoxLayout()
        hint = QLabel(
            "Every digit width from minimum through maximum is generated."
        )
        hint.setObjectName("mutedLabel")
        hint.setWordWrap(True)
        number_layout.addWidget(hint)
        number_layout.addWidget(self.number_panel)
        number_group.setLayout(number_layout)
        layout.addWidget(number_group)

        self.symbol_panel = SymbolPanel()
        symbol_group = QGroupBox("Symbols")
        symbol_layout = QVBoxLayout()
        symbol_layout.addWidget(self.symbol_panel)
        symbol_group.setLayout(symbol_layout)
        layout.addWidget(symbol_group)

        layout.addStretch()
        scroll.setWidget(content)
        page_layout.addWidget(scroll)

    def add_string(self, text=""):
        widget = StringInput(self.remove_string)
        if text:
            widget.text.setText(text)
        self.string_widgets.append(widget)
        self.string_layout.addWidget(widget)

    def remove_string(self, widget):
        if len(self.string_widgets) <= 1:
            widget.text.clear()
            return

        self.string_widgets.remove(widget)
        widget.deleteLater()

    def _clear_strings(self):
        for widget in list(self.string_widgets):
            widget.deleteLater()
        self.string_widgets.clear()

    def save_to_state(self):
        self.app_state.settings.base_strings.clear()

        for widget in self.string_widgets:
            text = widget.text.text().strip()
            if text:
                self.app_state.settings.base_strings.append(text)

        number = self.number_panel.get_settings()
        self.app_state.settings.use_numbers = number["enabled"]
        self.app_state.settings.min_length = number["min_length"]
        self.app_state.settings.max_length = number["max_length"]
        self.app_state.settings.range_from = number["range_from"]
        self.app_state.settings.range_to = number["range_to"]
        self.app_state.settings.zero_padding = number["zero_padding"]
        self.app_state.settings.permutations = number["permutations"]
        self.app_state.settings.number_order = number["order"]
        self.app_state.settings.symbols = self.symbol_panel.get_symbols()
        self.app_state.settings.symbol_mode = self.symbol_panel.get_mode()

    def load_from_state(self):
        settings = self.app_state.settings
        self._clear_strings()

        strings = settings.base_strings or [""]
        if not strings:
            strings = [""]
        for text in strings:
            self.add_string(text)

        self.number_panel.set_settings(settings)
        self.symbol_panel.set_settings(settings)
