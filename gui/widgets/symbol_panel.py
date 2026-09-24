from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QLineEdit,
    QLabel,
    QComboBox,
)


class SymbolPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.enable = QCheckBox("Enable Symbols")
        self.enable.setChecked(True)
        layout.addWidget(self.enable)

        layout.addWidget(QLabel("Symbol placement"))
        self.mode = QComboBox()
        self.mode.addItem("Prefix and suffix", "ends")
        self.mode.addItem("Suffix only", "suffix")
        self.mode.addItem("Prefix only", "prefix")
        self.mode.addItem("Wrap both sides", "wrap")
        self.mode.addItem("Every position", "all")
        layout.addWidget(self.mode)

        layout.addWidget(QLabel("Common symbols"))
        self.common_symbols = QLineEdit()
        self.common_symbols.setText("!@#$")
        layout.addWidget(self.common_symbols)

        layout.addWidget(QLabel("Custom symbols"))
        self.custom_symbols = QLineEdit()
        self.custom_symbols.setPlaceholderText("Add extra symbols")
        layout.addWidget(self.custom_symbols)

        self.enable.toggled.connect(self._toggle)

    def _toggle(self, enabled):
        self.mode.setEnabled(enabled)
        self.common_symbols.setEnabled(enabled)
        self.custom_symbols.setEnabled(enabled)

    def get_mode(self):
        return self.mode.currentData() or "ends"

    def get_symbols(self):
        if not self.enable.isChecked():
            return []

        symbols = []
        common = self.common_symbols.text().strip()
        if common:
            symbols.extend(list(common))

        custom = self.custom_symbols.text().strip()
        if custom:
            symbols.extend(list(custom))

        unique = []
        for symbol in symbols:
            if symbol not in unique:
                unique.append(symbol)
        return unique

    def set_settings(self, settings):
        symbols = settings.symbols or []
        self.enable.setChecked(bool(symbols))
        self.common_symbols.setText("".join(symbols))
        self.custom_symbols.clear()
        index = self.mode.findData(getattr(settings, "symbol_mode", "ends"))
        if index >= 0:
            self.mode.setCurrentIndex(index)
