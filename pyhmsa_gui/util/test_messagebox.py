#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa_gui.util.testcase import TestCaseQApp, QTest
from pyhmsa_gui.util.messagebox import exception, exceptions

# Globals and constants variables.

class TestModule(TestCaseQApp):

    def setUp(self):
        TestCaseQApp.setUp(self)

    def tearDown(self):
        TestCaseQApp.tearDown(self)

    def testexception(self):
        pass

    def testexceptions(self):
        pass

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
