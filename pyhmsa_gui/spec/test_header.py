#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.
from pyhmsa.spec.header import Header
from pyhmsa.type.checksum import Checksum

# Local modules.
from pyhmsa_gui.util.testcase import TestCaseQApp, QTest
from pyhmsa_gui.spec.header import HeaderWidget

# Globals and constants variables.

class TestHeaderWidget(TestCaseQApp):

    def setUp(self):
        TestCaseQApp.setUp(self)

        self.wdg = HeaderWidget()

        self.header = Header()
        self.header.title = 'Beep beep'
        self.header.author = 'Wyle E. Coyote'
        self.header.owner = 'Acme Inc.'
        self.header.date = '1985-10-26'
        self.header.time = '20:04:00'
        self.header.timezone = 'AUS Eastern Standard Time'
        self.header.checksum = \
            Checksum('53AAD59C05D59A40AD746D6928EA6D2D526865FD', 'SHA-1')

    def tearDown(self):
        TestCaseQApp.tearDown(self)

    def test_initui(self):
        QTest.keyClicks(self.wdg._txt_title, "Title")
        self.assertEqual("Title", self.wdg._txt_title.text())

        QTest.keyClicks(self.wdg._txt_author, 'Author')
        self.assertEqual("Author", self.wdg._txt_author.text())

        QTest.keyClicks(self.wdg._txt_owner, 'Owner')
        self.assertEqual("Owner", self.wdg._txt_owner.text())

        QTest.keyClicks(self.wdg._txt_timezone, 'Eastern')
        self.assertEqual("Eastern", self.wdg._txt_timezone.text())

        QTest.keyClicks(self.wdg._txt_checksum, 'check')
        self.assertIsNone(self.wdg._txt_checksum.text())

    def testsetHeader(self):
        self.wdg.setHeader(self.header)
        self.assertEqual("Beep beep", self.wdg._txt_title.text())
        self.assertEqual("Wyle E. Coyote", self.wdg._txt_author.text())
        self.assertEqual("Acme Inc.", self.wdg._txt_owner.text())
        self.assertEqual("1985-10-26", self.wdg._txt_date.text())
        self.assertEqual("20:04:00", self.wdg._txt_time.text())
        self.assertEqual("AUS Eastern Standard Time", self.wdg._txt_timezone.text())
        self.assertEqual('53AAD59C05D59A40AD746D6928EA6D2D526865FD', self.wdg._txt_checksum.text())

    def testheader(self):
        self.wdg.setHeader(self.header)
        header = self.wdg.header()

        self.assertEqual('Beep beep', header.title)
        self.assertEqual('Wyle E. Coyote', header.author)
        self.assertEqual('Acme Inc.', header.owner)
        self.assertEqual(1985, header.date.year)
        self.assertEqual(10, header.date.month)
        self.assertEqual(26, header.date.day)
        self.assertEqual(20, header.time.hour)
        self.assertEqual(4, header.time.minute)
        self.assertEqual(0, header.time.second)
        self.assertIsNone(header.checksum)

    def testsetReadOnly(self):
        QTest.keyClicks(self.wdg._txt_title, "Title")
        self.wdg.setReadOnly(True)

        self.assertTrue(self.wdg.isReadOnly())
        QTest.keyClicks(self.wdg._txt_title, "Title2")
        self.assertEqual("Title", self.wdg._txt_title.text())

    def testisReadOnly(self):
        self.assertFalse(self.wdg.isReadOnly())

    def testhasAcceptableInput(self):
        self.assertTrue(self.wdg.hasAcceptableInput())

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
