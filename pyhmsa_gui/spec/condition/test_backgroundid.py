#!/usr/bin/env python
""" """

# Standard library modules.
import logging
import unittest

# Third party modules.

# Local modules.
from pyhmsa_gui.util.testcase import TestCaseQApp
from pyhmsa_gui.spec.condition.backgroundid import BackgroundIDWidget


# Globals and constants variables.

class TestBackgroundIDWidget(TestCaseQApp):
    def setUp(self):
        TestCaseQApp.setUp(self)

        self.wdg = BackgroundIDWidget

    def tearDown(self):
        TestCaseQApp.tearDown(self)

    def test_initui(self):
        pass


if __name__ == '__main__':  # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
