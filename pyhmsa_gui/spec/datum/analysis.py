"""
Analysis widgets
"""

# Standard library modules.

# Third party modules.
from qtpy.QtCore import Qt, QAbstractTableModel

# Local modules.
from pyhmsa_gui.spec.datum.datum import _DatumTableWidget, _DatumFigureWidget
from pyhmsa_gui.util.mpl.toolbar import NavigationToolbarQT, NavigationToolbarSnapMixinQT

from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D
from pyhmsa.spec.condition.detector import DetectorSpectrometer

from pyhmsa_plot.spec.datum.analysis import Analysis1DPlot, Analysis2DPlot

# Globals and constants variables.

class _Analysis1DNagivationToolbarQT(NavigationToolbarSnapMixinQT,
                                     NavigationToolbarQT):

    def __init__(self, canvas, parent, coordinates=True):
        NavigationToolbarQT.__init__(self, canvas, parent, coordinates)
        NavigationToolbarSnapMixinQT.__init__(self)

    def _init_toolbar(self):
        NavigationToolbarQT._init_toolbar(self)
        NavigationToolbarSnapMixinQT._init_toolbar(self)

class Analysis0DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

        def rowCount(self, parent=None):
            return 1

        def columnCount(self, parent=None):
            return 1

        def data(self, index, role):
            if not index.isValid() or not (0 <= index.row() < 1):
                return None
            if role != Qt.DisplayRole:
                return None

            return str(self._datum)

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                return 'Value'
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def __init__(self, controller, datum=None, parent=None):
        _DatumTableWidget.__init__(self, Analysis0D, controller, datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class Analysis1DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

            conditions = datum.conditions.findvalues(DetectorSpectrometer)
            if conditions:
                self._calibration = next(iter(conditions)).calibration
            else:
                self._calibration = None

        def rowCount(self, parent=None):
            return self._datum.channels

        def columnCount(self, parent=None):
            return 2 if self._calibration is not None else 1

        def data(self, index, role):
            if not index.isValid() or not (0 <= index.row() < self._datum.channels):
                return None
            if role != Qt.DisplayRole:
                return None

            row = index.row()
            column = index.column()
            if self._calibration is not None:
                if column == 0:
                    return str(self._calibration(row))
                elif column == 1:
                    return str(self._datum[row])
            else:
                return str(self._datum[row])

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                if self._calibration is not None:
                    if section == 0:
                        return '%s (%s)' % (self._calibration.quantity,
                                            self._calibration.unit)
                    elif section == 1:
                        return 'Value'
                else:
                    return 'Value'
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def __init__(self, controller, datum=None, parent=None):
        _DatumTableWidget.__init__(self, Analysis1D, controller, datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class Analysis1DGraphWidget(_DatumFigureWidget):

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, Analysis1DPlot, Analysis1D,
                                    controller, datum, parent)

    def _create_toolbar(self, canvas):
        return _Analysis1DNagivationToolbarQT(canvas, self.parent())

class Analysis2DTableWidget(_DatumTableWidget):

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

        def rowCount(self, parent=None):
            return self._datum.v

        def columnCount(self, parent=None):
            return self._datum.u

        def data(self, index, role):
            if not index.isValid() or \
                    not (0 <= index.row() < self._datum.v) or \
                    not (0 <= index.column() < self._datum.u):
                return None
            if role != Qt.DisplayRole:
                return None

            row = index.row()
            column = index.column()
            return str(self._datum[column, row])

        def headerData(self, section , orientation, role):
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                return str(section + 1)
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def __init__(self, controller, datum=None, parent=None):
        _DatumTableWidget.__init__(self, Analysis2D, controller, datum, parent)

    def _create_model(self, datum):
        return self._TableModel(datum)

class Analysis2DGraphWidget(_DatumFigureWidget):

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, Analysis2DPlot, Analysis2D,
                                    controller, datum, parent)
