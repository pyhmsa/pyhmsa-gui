"""
Extension of matplotlib backend
"""

# Standard library modules.
import os

# Third party modules.
import six

import numpy as np

from qtpy.QtWidgets import \
    (QAction, QCheckBox, QLabel, QFileDialog, QSpinBox, QHBoxLayout,
     QMessageBox)

import matplotlib
from matplotlib.backends.backend_qt5 import \
    NavigationToolbar2QT as _NavigationToolbar2QT

# Local modules.
from pyhmsa_gui.util.icon import getIcon

# Globals and constants variables.

class _SaveDialog(QFileDialog):

    def __init__(self, parent):
        QFileDialog.__init__(self, parent)
        self.setFileMode(QFileDialog.AnyFile)
        self.setAcceptMode(QFileDialog.AcceptSave)

        # Widgets
        self._chk_tight = QCheckBox('Tight layout')

        self._txt_dpi = QSpinBox()
        self._txt_dpi.setRange(1, 10000)
        self._txt_dpi.setSingleStep(50)
        self._txt_dpi.setSuffix('dpi')
        self._txt_dpi.setValue(100)

        # Layouts
        layout = self.layout()

        lyt_extras = QHBoxLayout()
        lyt_extras.addWidget(QLabel('Extra options'))
        lyt_extras.addWidget(self._chk_tight)
        lyt_extras.addWidget(QLabel('Resolution'))
        lyt_extras.addWidget(self._txt_dpi)
        layout.addLayout(lyt_extras, layout.rowCount(), 0, 1, layout.columnCount())

        self.setLayout(layout)

    def tightLayout(self):
        return self._chk_tight.isChecked()

    def setTightLayout(self, tight):
        self._chk_tight.setChecked(tight)

    def dpi(self):
        return self._txt_dpi.value()

    def setDpi(self, dpi):
        self._txt_dpi.setValue(dpi)

class NavigationToolbarQT(_NavigationToolbar2QT):

    def _get_save_name_filters(self):
        filters = []
        selected_filter = None
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = list(six.iteritems(filetypes))
        sorted_filetypes.sort()
        default_filetype = self.canvas.get_default_filetype()

        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter_ = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selected_filter = filter_
            filters.append(filter_)

        return filters, selected_filter

    def save_figure(self, *args):
        dialog = _SaveDialog(self.parent)
        dialog.setWindowTitle("Choose a filename to save to")
        dialog.setDpi(matplotlib.rcParams.get('savefig.dpi',
                                              self.canvas.figure.dpi))
        dialog.setTightLayout(matplotlib.rcParams.get('savefig.bbox', None) == 'tight')

        filters, selected_filter = self._get_save_name_filters()
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(selected_filter)

        startpath = matplotlib.rcParams.get('savefig.directory', '')
        startpath = os.path.expanduser(startpath)
        start = os.path.join(startpath, self.canvas.get_default_filename())
        dialog.selectFile(start)

        if not dialog.exec_():
            return

        fnames = dialog.selectedFiles()
        if len(fnames) != 1:
            return
        fname = fnames[0]

        dpi = dialog.dpi()
        bbox_inches = 'tight' if dialog.tightLayout() else None

        # Store default values
        if startpath == '':
            # explicitly missing key or empty str signals to use cwd
            matplotlib.rcParams['savefig.directory'] = startpath
        else:
            # save dir for next time
            savefig_dir = os.path.dirname(six.text_type(fname))
            matplotlib.rcParams['savefig.directory'] = savefig_dir

        matplotlib.rcParams['savefig.dpi'] = dpi
        matplotlib.rcParams['savefig.bbox'] = bbox_inches

        # Save
        try:
            self.canvas.print_figure(six.text_type(fname),
                                 dpi=dpi, bbox_inches=bbox_inches)
        except Exception as e:
            QMessageBox.critical(
                self, "Error saving file", str(e),
                QMessageBox.Ok, QMessageBox.NoButton)

class NavigationToolbarSnapMixin(object):

    def __init__(self):
        self._snap_cross = {}

    def _clear_snap(self):
        for axes, (crossh, crossv) in self._snap_cross.items():
            axes.lines.remove(crossh)
            axes.lines.remove(crossv)
        self._snap_cross.clear()
        self.draw()

    def pan(self, *args):
        self._clear_snap()
        super().pan(*args)

    def zoom(self, *args):
        print('xoom')
        self._clear_snap()
        super().zoom(*args)

    def snap(self, *args):
        if self._active == 'SNAP':
            self._active = None
        else:
            self._active = 'SNAP'

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)

        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)

        self._clear_snap()

        if self._active:
            self.mode = 'snap'
            self.canvas.widgetlock(self)

            for axes in self.canvas.figure.get_axes():
                xmin, _ = axes.get_xlim()
                ymin, _ = axes.get_ylim()
                color = matplotlib.rcParams.get('snap.color', 'r')
                lw = matplotlib.rcParams.get('snap.linewidth', 2)
                crossh = axes.axhline(ymin, color=color, lw=lw)
                crossv = axes.axvline(xmin, color=color, lw=lw)
                crossh.set_visible(False)
                crossv.set_visible(False)
                self._snap_cross[axes] = (crossh, crossv)
        else:
            self.mode = ''
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)

    def mouse_move(self, event):
        if self.mode != 'snap':
            super().mouse_move(event)
            return

        for axes, (crossh, crossv) in self._snap_cross.items():
            crossh.set_visible(event.inaxes == axes)
            crossv.set_visible(event.inaxes == axes)

        if event.inaxes is None:
            super().mouse_move(event)
            self.draw()
            return

        x = event.xdata
        y = event.ydata

        xlines = []
        ylines = []
        for line in event.inaxes.lines:
            if line in self._snap_cross[event.inaxes]: continue
            xs = line.get_xdata()
            ys = line.get_ydata()
            index = np.abs(xs - x).argmin()
            xlines.append(xs[index])
            ylines.append(ys[index])

        index = np.abs(np.array(ylines) - y).argmin()
        x = xlines[index]
        y = ylines[index]

        crossh, crossv = self._snap_cross[event.inaxes]
        crossh.set_ydata([y, y])
        crossv.set_xdata([x, x])

        s = event.inaxes.format_coord(x, y)
        self.set_message('%s, %s' % (self.mode, s))

        self.draw()

class NavigationToolbarSnapMixinQT(NavigationToolbarSnapMixin):

    def _init_toolbar(self):
        a = QAction(getIcon('snap'), 'Snap', self)
        a.setCheckable(True)
        a.setToolTip('Snap to data')
        a.triggered.connect(self.snap)
        self._actions['snap'] = a
        self.insertAction(self._actions['pan'], a)

    def snap(self, *args):
        super().snap(*args)
        self._update_buttons_checked()

    def _update_buttons_checked(self):
        super()._update_buttons_checked()
        self._actions['snap'].setChecked(self._active == 'SNAP')

class NavigationToolbarColorbarMixinQT(object):

    def _init_toolbar(self):
        a = QAction(getIcon('color-wheel'), 'Color bar', self)
        a.setToolTip('Add color bar')
        a.setCheckable(True)
        a.triggered.connect(self.colorbar)
        self._actions['colorbar'] = a
        self.insertAction(self._actions['configure_subplots'], a)

    def colorbar(self, *args):
        raise NotImplementedError

    def isColorbarChecked(self):
        return self._actions['colorbar'].isChecked()

class NavigationToolbarScalebarMixinQT(object):

    def _init_toolbar(self):
        a = QAction(getIcon('ruler'), 'Scale bar', self)
        a.setToolTip('Add scale bar')
        a.setCheckable(True)
        a.triggered.connect(self.scalebar)
        self._actions['scalebar'] = a
        self.insertAction(self._actions['configure_subplots'], a)

    def scalebar(self):
        raise NotImplementedError

    def isScalebarChecked(self):
        return self._actions['scalebar'].isChecked()

