#!/usr/bin/env python
""" """

# Standard library modules.
import unittest

# Third party modules.
from qtpy import QtCore, QtGui, QtWidgets

from qtpy.QtTest import QTest #@UnusedImport

# Local modules.
from pyhmsa_gui.util.settings import Settings

# Globals and constants variables.

class MockController(QtCore.QObject):

    def __init__(self):
        self._settings = Settings("HMSA", "testcase")

    @property
    def settings(self):
        return self._settings

_instance = None

class TestCaseQApp(unittest.TestCase):
    '''Helper class to provide QApplication instances'''

    qapplication = True

    def setUp(self):
        super().setUp()
        if isinstance(QtGui.qApp, type(None)):
            self.app = QtWidgets.QApplication([])
        else:
            self.app = QtGui.qApp

        self.controller = MockController()

    def tearDown(self):
        '''Deletes the reference owned by self'''
        del self.app
        super().tearDown()
