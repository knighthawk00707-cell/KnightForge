from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QCheckBox,
    QSpinBox,
    QComboBox,
)


class NumberPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QFormLayout(self)

        # Enable numbers
        self.enable = QCheckBox("Enable Numbers")
        self.enable.setChecked(True)

        # Number length
        self.min_len = QSpinBox()
        self.min_len.setRange(1, 20)
        self.min_len.setValue(1)

        self.max_len = QSpinBox()
        self.max_len.setRange(1, 20)
        self.max_len.setValue(4)

        self.min_len.setToolTip(
            "Shortest number of digits. Every width from this value "
            "through Maximum Length is generated."
        )
        self.max_len.setToolTip(
            "Longest number of digits. Combined with Minimum Length, "
            "this is the full range of number widths in the wordlist."
        )

        # Numeric range
        self.range_from = QSpinBox()
        self.range_from.setMaximum(999999999)
        self.range_from.setValue(0)

        self.range_to = QSpinBox()
        self.range_to.setMaximum(999999999)
        self.range_to.setValue(9999)

        # Zero Padding
        self.zero_padding = QCheckBox()
        self.zero_padding.setChecked(True)

        # Generate all permutations
        self.permutations = QCheckBox()

        # Generation order
        self.order = QComboBox()
        self.order.addItems([
            "Ascending",
            "Descending",
            "Random"
        ])

        self.min_len.valueChanged.connect(self._keep_length_order)
        self.max_len.valueChanged.connect(self._keep_length_order)

        layout.addRow(self.enable)
        layout.addRow("Minimum Length", self.min_len)
        layout.addRow("Maximum Length", self.max_len)
        layout.addRow("Range From", self.range_from)
        layout.addRow("Range To", self.range_to)
        layout.addRow("Zero Padding", self.zero_padding)
        layout.addRow("Permutations", self.permutations)
        layout.addRow("Order", self.order)

    def _keep_length_order(self):
        if self.min_len.value() > self.max_len.value():
            self.max_len.setValue(self.min_len.value())

    def get_settings(self):
        """Return all settings as a dictionary."""
        return {
            "enabled": self.enable.isChecked(),
            "min_length": self.min_len.value(),
            "max_length": self.max_len.value(),
            "range_from": self.range_from.value(),
            "range_to": self.range_to.value(),
            "zero_padding": self.zero_padding.isChecked(),
            "permutations": self.permutations.isChecked(),
            "order": self.order.currentText(),
        }

    def set_settings(self, settings):
        self.enable.setChecked(settings.use_numbers)
        self.min_len.setValue(settings.min_length)
        self.max_len.setValue(settings.max_length)
        self.range_from.setValue(settings.range_from)
        self.range_to.setValue(settings.range_to)
        self.zero_padding.setChecked(settings.zero_padding)
        self.permutations.setChecked(settings.permutations)
        index = self.order.findText(settings.number_order)
        if index >= 0:
            self.order.setCurrentIndex(index)