"""
Analysis list widgets
"""

# Standard library modules.

# Third party modules.
from qtpy.QtWidgets import QSlider, QFormLayout
from qtpy.QtCore import Qt

# Local modules.
from pyhmsa_gui.spec.datum.datum import _DatumWidget, _DatumFigureWidget
from pyhmsa_gui.spec.datum.analysis import \
    (Analysis0DTableWidget, Analysis1DGraphWidget, Analysis1DTableWidget,
     Analysis2DGraphWidget, Analysis2DTableWidget)

from pyhmsa.spec.datum.analysislist import \
    AnalysisList0D, AnalysisList1D, AnalysisList2D

from pyhmsa_plot.spec.datum.analysislist import AnalysisList0DPlot

# Globals and constants variables.

class _AnalysisListWidget(_DatumWidget):

    def __init__(self, clasz, controller, datum=None, parent=None):
        self._datum = datum
        _DatumWidget.__init__(self, clasz, controller, datum, parent)

    def _init_ui(self):
        # Widgets
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setTickPosition(QSlider.TicksBelow)

        self._wdg_analysis = self._create_analysis_widget()

        # Layouts
        layout = _DatumWidget._init_ui(self)

        sublayout = QFormLayout()
        sublayout.addRow('Analyses', self._slider)
        layout.addLayout(sublayout)

        layout.addWidget(self._wdg_analysis)

        # Signals
        self._slider.valueChanged.connect(self._on_slide)

        return layout

    def _create_analysis_widget(self):
        raise NotImplementedError

    def _on_slide(self, value):
        if self._datum is None:
            return
        analysis = self._datum.toanalysis(value)
        self._wdg_analysis.setDatum(analysis)

    def setDatum(self, datum):
        _DatumWidget.setDatum(self, datum)
        self._datum = datum

        maximum = datum.analysis_count - 1 if datum is not None else 0
        self._slider.setMaximum(maximum)
        self._slider.setValue(0)
        self._on_slide(0)

class AnalysisList0DTableWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList0D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis0DTableWidget(self.controller)

class AnalysisList0DGraphWidget(_DatumFigureWidget):

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, AnalysisList0DPlot, AnalysisList0D,
                                    controller, datum, parent)

class AnalysisList1DTableWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList1D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis1DTableWidget(self.controller)

class AnalysisList1DGraphWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList1D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis1DGraphWidget(self.controller)

class AnalysisList2DTableWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList2D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis2DTableWidget(self.controller)

class AnalysisList2DGraphWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList2D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis2DGraphWidget(self.controller)
