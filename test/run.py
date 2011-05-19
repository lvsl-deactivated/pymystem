#!/usr/bin/env python

import unittest

import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_lib_tests():
    from lib_tests import suite
    unittest.TextTestRunner().run(suite())

def run_mystem_tests():
    from mystem_tests import suite
    unittest.TextTestRunner().run(suite())

def main():
    run_lib_tests()
    run_mystem_tests()

if __name__ == "__main__":
    main()
