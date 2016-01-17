#!/usr/bin/env python
""" """

# Standard library modules.
import unittest

# Third party modules.
from qtpy.QtWidgets import QApplication

# Local modules.

# Globals and constants variables.

_instance = None

class TestCaseQApp(unittest.TestCase):
    '''Helper class to provide QApplication instances'''

    qapplication = True

    def setUp(self):
        super().setUp()
        global _instance
        if _instance is None:
            _instance = QApplication([])

        self.app = _instance

    def tearDown(self):
        '''Deletes the reference owned by self'''
        del self.app
        super().tearDown()
