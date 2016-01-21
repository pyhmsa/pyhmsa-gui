#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.gui.util.testcase import TestCaseQApp
from pyhmsa.gui.util.icon import getIcon

# Globals and constants variables.

class TestModule(TestCaseQApp):

    def setUp(self):
        TestCaseQApp.setUp(self)

    def tearDown(self):
        TestCaseQApp.tearDown(self)

    def testgetIcon(self):
        icon = getIcon('document-new')
        self.assertFalse(icon.isNull())

        icon = getIcon('document-newwwww')
        self.assertTrue(icon.isNull())

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
