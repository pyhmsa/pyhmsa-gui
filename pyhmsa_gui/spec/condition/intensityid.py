"""
IntensityID widget
"""

# Standard library modules.

# Third party modules.
from qtpy.QtWidgets import QComboBox

# Local modules.
from pyhmsa_gui.spec.condition.condition import _ConditionWidget

from pyhmsa_measurement.spec.condition.intensityid import \
    IntensityID, _INTENSITY_TYPES, _INTENSITY_MEASURES


# Globals and constants variables.

class IntensityIDWidget(_ConditionWidget):
    def __init__(self, parent=None):
        _ConditionWidget.__init__(self, IntensityID, parent)

    def _init_ui(self):
        print("TEST HUHU")
        # Controls
        self._cb_type = QComboBox()
        self._cb_type.addItems([None] + list(_INTENSITY_TYPES))
        self._cb_measure = QComboBox()
        self._cb_measure.addItems([None] + list(_INTENSITY_MEASURES))

        # Layouts
        layout = _ConditionWidget._init_ui(self)
        layout.addRow("<i>Type</i>", self._cb_type)
        layout.addRow("<i>Measure</i>", self._cb_measure)

        # Signals
        self._cb_type.currentIndexChanged.connect(self.edited)
        self._cb_measure.currentIndexChanged.connect(self.edited)

        return layout

    def _create_parameter(self):
        return self.CLASS(None, None)

    def parameter(self, parameter=None):
        parameter = _ConditionWidget.parameter(self, parameter)
        parameter.type = self._cb_type
        parameter.measure = self._cb_measure
        return parameter

    def setParameter(self, condition):
        _ConditionWidget.setParameter(self, condition)
        self._cb_type.setCurrentIndex(self._cb_type.findText(condition.type))
        self._cb_measure.setCurrentIndex(self._cb_measure.findText(condition.measure))

    def setReadOnly(self, state):
        _ConditionWidget.setReadOnly(self, state)
        self._cb_type.setEnabled(not state)
        self._cb_measure.setEnabled(not state)

    def isReadOnly(self):
        return _ConditionWidget.isReadOnly(self) and \
               not self._cb_type.isEnabled() and \
               not self._cb_measure.isEnabled()

    def hasAcceptableInput(self):
        return _ConditionWidget.hasAcceptableInput(self)
