#!/usr/bin/env python

import unittest
from mock import Mock, patch
import sys
import os
from src.console_controller import ConsoleController

class TestConsoleController(unittest.TestCase):

    def setUp(self):
        self.ctrlr = ConsoleController()

    def test_constructor(self):
        self.assertEqual('ConsoleController', self.ctrlr.__class__.__name__)

    def test_read_fasta(self):
        self.assertFalse(self.ctrlr.genome.fasta)
        self.assertFalse(self.ctrlr.fasta_file)
        self.ctrlr.read_fasta("demo/demo.fasta")
        self.assertTrue(self.ctrlr.genome.fasta)
        # ctrlr should retain fastas filename
        self.assertEquals("demo/demo.fasta", self.ctrlr.fasta_file)

    def test_read_gff(self):
        self.assertFalse(self.ctrlr.genome.gff)
        self.ctrlr.read_gff("demo/demo.gff")
        self.assertTrue(self.ctrlr.genome.gff)

    def test_prep_tbl2asn(self):
        self.assertFalse(os.path.isdir("tbl2asn_unittest"))
        # must have a fasta, a tbl and an sbt
        self.ctrlr.read_fasta("demo/demo.fasta")
        self.ctrlr.read_gff("demo/demo.gff")
        self.ctrlr.genome.add_template_file("demo/demo.sbt")
        self.ctrlr.prep_tbl2asn("tbl2asn_unittest")
        self.assertTrue(os.path.isdir("tbl2asn_unittest"))
        self.assertTrue(os.path.exists("tbl2asn_unittest/gag.sbt"))
        self.assertTrue(os.path.exists("tbl2asn_unittest/gag.fsa"))
        self.assertTrue(os.path.exists("tbl2asn_unittest/gag.tbl"))
        os.system('rm -r tbl2asn_unittest')

   
    def test_ready_for_tbl2asn(self):
        self.ctrlr.set_tbl2asn_executable("actual/path/goes/here")
        def no_fsa(path):
            if path == "tbl2asn_demo/gag.fsa":
                return False
            else:
                return True
        def no_tbl(path):
            if path == "tbl2asn_demo/gag.tbl":
                return False
            else:
                return True
        def no_sbt(path):
            if path == "tbl2asn_demo/gag.sbt":
                return False
            else:
                return True
        self.assertTrue(self.ctrlr.ready_for_tbl2asn('tbl2asn_demo'))
        mock1 = Mock(side_effect=no_fsa)
        with patch('os.path.exists', mock1):
            self.assertFalse(self.ctrlr.ready_for_tbl2asn('tbl2asn_demo'))
        mock2 = Mock(side_effect=no_tbl)
        with patch('os.path.exists', mock2):
            self.assertFalse(self.ctrlr.ready_for_tbl2asn('tbl2asn_demo'))
        mock3 = Mock(side_effect=no_sbt)
        with patch('os.path.exists', mock3):
            self.assertFalse(self.ctrlr.ready_for_tbl2asn('tbl2asn_demo'))
        self.assertTrue(self.ctrlr.ready_for_tbl2asn('tbl2asn_demo'))
        


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConsoleController))
    return suite

if __name__ == '__main__':
    unittest.main()
