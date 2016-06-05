"""
BackgroundID widget
"""

# Standard library modules.

# Third party modules.
from qtpy.QtWidgets import QComboBox

# Local modules.
from pyhmsa_gui.spec.condition.condition import _ConditionWidget

from pyhmsa_measurement.spec.condition.backgroundid import \
    BackgroundID, _BACKGROUND_INTERPOLATIONS, BACKGROUND_INTERPOLATION_LINEAR


# Globals and constants variables.

class BackgroundIDWidget(_ConditionWidget):
    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, BackgroundID, parent)

    def _init_ui(self):
        # Controls
        self._cb_interpolation = QComboBox()
        self._cb_interpolation.addItems(list(_BACKGROUND_INTERPOLATIONS))

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow("<i>Interpolation</i>", self._cb_interpolation)

        # Signals
        self._cb_interpolation.currentIndexChanged.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(BACKGROUND_INTERPOLATION_LINEAR) # Temporary value

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.interpolation = self._cb_interpolation.currentText()
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        index = self._cb_interpolation.findText(condition.interpolation)
        self._cb_interpolation.setCurrentIndex(index)

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._cb_interpolation.setEnabled(not state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
               not self._cb_interpolation.isEnabled()
