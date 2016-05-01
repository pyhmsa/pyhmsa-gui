"""
Image raster widgets
"""

# Standard library modules.

# Third party modules.
from qtpy.QtWidgets import \
    QSlider, QFormLayout, QHBoxLayout, QRadioButton, QSplitter, QSizePolicy
from qtpy.QtCore import Qt, QAbstractTableModel, Signal

import numpy as np

# Local modules.
from pyhmsa_gui.spec.datum.datum import \
    _DatumWidget, _DatumTableWidget, _DatumFigureWidget
from pyhmsa_gui.spec.datum.analysis import \
    Analysis1DTableWidget, Analysis1DGraphWidget

from pyhmsa.spec.datum.analysis import Analysis1D
from pyhmsa.spec.datum.imageraster import ImageRaster2D, ImageRaster2DSpectral
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

from pyhmsa_plot.spec.datum.imageraster import ImageRaster2DPlot

# Globals and constants variables.

#class _ImageRaster2DNavigationToolbarQT(NavigationToolbarColorbarMixinQT,
#                                        NavigationToolbarScalebarMixinQT,
#                                        NavigationToolbarQT):
#
#    def __init__(self, canvas, parent, coordinates=True):
#        NavigationToolbarQT.__init__(self, canvas, parent, coordinates)
#        NavigationToolbarColorbarMixinQT.__init__(self)
#        NavigationToolbarScalebarMixinQT.__init__(self)
#
#    def _init_toolbar(self):
#        NavigationToolbarQT._init_toolbar(self)
#        NavigationToolbarColorbarMixinQT._init_toolbar(self)
#        NavigationToolbarScalebarMixinQT._init_toolbar(self)

class ImageRaster2DTableWidget(_DatumTableWidget):

    valueSelected = Signal(int, int)

    class _TableModel(QAbstractTableModel):

        def __init__(self, datum):
            QAbstractTableModel.__init__(self)
            self._datum = datum

        def rowCount(self, parent=None):
            return self._datum.y

        def columnCount(self, parent=None):
            return self._datum.x

        def data(self, index, role):
            if not index.isValid() or \
                    not (0 <= index.row() < self._datum.y) or \
                    not (0 <= index.column() < self._datum.x):
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
        _DatumTableWidget.__init__(self, ImageRaster2D, controller,
                                   datum, parent)

    def _init_ui(self):
        layout = _DatumTableWidget._init_ui(self)
        self._table.clicked.connect(self._on_table_clicked)
        return layout

    def _create_model(self, datum):
        return self._TableModel(datum)

    def _on_table_clicked(self, index):
        self.valueSelected.emit(index.column(), index.row())

class ImageRaster2DGraphWidget(_DatumFigureWidget):

    valueSelected = Signal(int, int)

    def __init__(self, controller, datum=None, parent=None):
        _DatumFigureWidget.__init__(self, ImageRaster2DPlot, ImageRaster2D,
                                    controller, datum, parent)

    def _init_ui(self):
        layout = _DatumFigureWidget._init_ui(self)
        self._canvas.mpl_connect("button_release_event", self._on_figure_clicked)
        return layout

    def _on_figure_clicked(self, event):
        if not event.inaxes or self._datum is None:
            return
        x = event.xdata
        y = event.ydata
        unit = self._create_plot().unit
        position = SpecimenPosition(x=(x, unit), y=(y, unit))
        x, y = self._datum.get_index(position)
        self.valueSelected.emit(x, y)

class _ImageRaster2DSpectralWidget(_DatumWidget):

    MODE_SUM = 'sum'
    MODE_MAX = 'max'
    MODE_SINGLE = 'single'
    MODE_RANGE = 'range'

    def __init__(self, controller, datum=None, parent=None):
        self._datum = datum
        _DatumWidget.__init__(self, ImageRaster2DSpectral, controller,
                              datum, parent)

    def _init_ui(self):
        # Widgets
        self._rdb_sum = QRadioButton("Sum")
        self._rdb_sum.setChecked(True)
        self._rdb_max = QRadioButton("Maximum")
        self._rdb_single = QRadioButton("Single")
        self._rdb_range = QRadioButton("Range")

        self._sld_start = QSlider(Qt.Horizontal)
        self._sld_start.setTickPosition(QSlider.TicksBelow)
        self._sld_start.setEnabled(False)

        self._sld_end = QSlider(Qt.Horizontal)
        self._sld_end.setTickPosition(QSlider.TicksBelow)
        self._sld_end.setEnabled(False)

        self._wdg_imageraster2d = self._create_imageraster2d_widget()
        self._wdg_analysis = self._create_analysis1d_widget()

        # Layouts
        layout = _DatumWidget._init_ui(self)

        sublayout = QHBoxLayout()
        sublayout.addWidget(self._rdb_sum)
        sublayout.addWidget(self._rdb_max)
        sublayout.addWidget(self._rdb_single)
        sublayout.addWidget(self._rdb_range)
        layout.addLayout(sublayout)

        sublayout = QFormLayout()
        sublayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow) # Fix for Mac OS
        sublayout.addRow('Channels (Start)', self._sld_start)
        sublayout.addRow('Channels (End)', self._sld_end)
        layout.addLayout(sublayout)

        splitter = QSplitter()
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(self._wdg_imageraster2d)
        splitter.addWidget(self._wdg_analysis)
        layout.addWidget(splitter)

        # Signals
        self._rdb_sum.toggled.connect(self._on_mode_sum)
        self._rdb_max.toggled.connect(self._on_mode_max)
        self._rdb_single.toggled.connect(self._on_mode_single)
        self._rdb_range.toggled.connect(self._on_mode_range)

        self._sld_start.valueChanged.connect(self._on_slide_start)
        self._sld_end.valueChanged.connect(self._on_slide_end)

        self._wdg_imageraster2d.valueSelected.connect(self._on_value_selected)

        # Defaults
        self.setMode(self.MODE_SUM)

        return layout

    def _create_analysis1d_widget(self):
        raise NotImplementedError

    def _create_imageraster2d_widget(self):
        raise NotImplementedError

    def _on_mode_sum(self, checked):
        if checked:
            self.setMode(self.MODE_SUM)

    def _on_mode_max(self, checked):
        if checked:
            self.setMode(self.MODE_MAX)

    def _on_mode_single(self, checked):
        if checked:
            self.setMode(self.MODE_SINGLE)

    def _on_mode_range(self, checked):
        if checked:
            self.setMode(self.MODE_RANGE)

    def _update_data(self, mode=None):
        if mode is None:
            mode = self.mode()

        if mode == self.MODE_SUM:
            self._update_mode_sum()
        elif mode == self.MODE_MAX:
            self._update_mode_max()
        elif mode == self.MODE_SINGLE:
            self._update_mode_single()
        elif mode == self.MODE_RANGE:
            self._update_mode_range()

    def _update_mode_sum(self):
        if self._datum is None:
            return
        subdatum = np.sum(self._datum, 2)
        self._wdg_imageraster2d.setDatum(subdatum)

    def _update_mode_max(self):
        if self._datum is None:
            return
        subdatum = np.amax(self._datum, 2)
        self._wdg_imageraster2d.setDatum(subdatum)

    def _update_mode_single(self):
        if self._datum is None:
            return
        channel = self._sld_start.value()
        subdatum = self._datum[:, :, channel]
        self._wdg_imageraster2d.setDatum(subdatum)

    def _update_mode_range(self):
        if self._datum is None:
            return
        start = self._sld_start.value()
        end = self._sld_end.value()
        start2 = min(start, end)
        end2 = max(start, end)
        subdatum = np.sum(self._datum[:, :, start2:end2 + 1], 2)
        self._wdg_imageraster2d.setDatum(subdatum)

    def _on_slide_start(self, channel):
        if self._rdb_single.isChecked():
            self._update_mode_single()
        elif self._rdb_range.isChecked():
            self._update_mode_range()

    def _on_slide_end(self, channel):
        self._update_mode_range()

    def _on_value_selected(self, x, y):
        if self._datum is None:
            return
        subdatum = self._datum[x, y]
        self._wdg_analysis.setDatum(subdatum.view(Analysis1D))

    def setDatum(self, datum):
        _DatumWidget.setDatum(self, datum)
        self._datum = datum

        maximum = datum.channels - 1 if datum is not None else 0
        self._sld_start.setMaximum(maximum)
        self._sld_end.setMaximum(maximum)

        self._update_data()

    def setMode(self, mode):
        rsum = rmax = rsingle = rrange = False
        sstart = send = False
        if mode == self.MODE_SUM:
            rsum = True
        elif mode == self.MODE_MAX:
            rmax = True
        elif mode == self.MODE_SINGLE:
            rsingle = True
            sstart = True
        elif mode == self.MODE_RANGE:
            rrange = True
            sstart = send = True
        else:
            raise ValueError('Unknown mode')

        self._rdb_sum.setChecked(rsum)
        self._rdb_max.setChecked(rmax)
        self._rdb_single.setChecked(rsingle)
        self._rdb_range.setChecked(rrange)
        self._sld_start.setEnabled(sstart)
        self._sld_end.setEnabled(send)

        self._update_data(mode)

    def mode(self):
        if self._rdb_sum.isChecked():
            return self.MODE_SUM
        elif self._rdb_max.isChecked():
            return self.MODE_MAX
        elif self._rdb_single.isChecked():
            return self.MODE_SINGLE
        elif self._rdb_range.isChecked():
            return self.MODE_RANGE
        else:
            raise ValueError('Unknown mode')

class ImageRaster2DSpectralTableWidget(_ImageRaster2DSpectralWidget):

    def _create_imageraster2d_widget(self):
        return ImageRaster2DTableWidget(self.controller)

    def _create_analysis1d_widget(self):
        return Analysis1DTableWidget(self.controller)

class _Analysis1DGraphWidget2(Analysis1DGraphWidget):

    def __init__(self, controller, datum=None, parent=None):
        self._draw_position = False
        self._selected_position = None
        self._draw_range = False
        self._selected_range = None
        Analysis1DGraphWidget.__init__(self, controller, datum, parent)

    def _create_plot(self):
        plot = Analysis1DGraphWidget._create_plot(self)

        if self._draw_position and self._selected_position is not None:
            plot.add_selected_x(self._selected_position)

        if self._draw_range and self._selected_range is not None:
            plot.add_selected_range(*self._selected_range)

        return plot

    def setMode(self, mode):
        self._draw_range = self._draw_position = False
        if mode == _ImageRaster2DSpectralWidget.MODE_SINGLE:
            self._draw_position = True
        elif mode == _ImageRaster2DSpectralWidget.MODE_RANGE:
            self._draw_range = True

        self._update_plot()

    def setSinglePosition(self, channel):
        if self._datum is None:
            return

        xs = self._datum.get_xy()[:, 0]
        self._selected_position = xs[channel]
        self._draw_position = True

        self._update_plot()

    def setRange(self, start, end):
        if self._datum is None:
            return

        xs = self._datum.get_xy()[:, 0]
        xmin = xs[start]; xmax = xs[end]
        self._selected_range = (xmin, xmax)
        self._draw_range = True

        self._update_plot()

class ImageRaster2DSpectralGraphWidget(_ImageRaster2DSpectralWidget):

    def _create_imageraster2d_widget(self):
        return ImageRaster2DGraphWidget(self.controller)

    def _create_analysis1d_widget(self):
        return _Analysis1DGraphWidget2(self.controller)

    def _update_mode_single(self):
        _ImageRaster2DSpectralWidget._update_mode_single(self)

        channel = self._sld_start.value()
        self._wdg_analysis.setSinglePosition(channel)

    def _update_mode_range(self):
        _ImageRaster2DSpectralWidget._update_mode_range(self)

        start = self._sld_start.value()
        end = self._sld_end.value()
        self._wdg_analysis.setRange(start, end)

    def setMode(self, mode):
        _ImageRaster2DSpectralWidget.setMode(self, mode)
        self._wdg_analysis.setMode(mode)


