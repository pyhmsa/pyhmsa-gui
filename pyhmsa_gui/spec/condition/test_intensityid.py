#!/usr/bin/env python
""" """

# Standard library modules.
import logging
import unittest

# Third party modules.

# Local modules.
from pyhmsa_gui.util.testcase import TestCaseQApp
from pyhmsa_gui.spec.condition.intensityid import IntensityIDWidget


# Globals and constants variables.

class TestIntensityIDWidget(TestCaseQApp):
    def setUp(self):
        TestCaseQApp.setUp(self)

        self.wdg = IntensityIDWidget()

    def tearDown(self):
        TestCaseQApp.tearDown(self)

    def test_initui(self):
        pass


if __name__ == '__main__':  # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
