#!/usr/bin/env python
"""
RollSmart Unit Tests
"""
import os
import re
import time
import unittest

from rollsmart.scripts.rollsmart import RollSmart

class RollsmartTest(unittest.Testcase):
    """
    Class of unit tests to verify the functionality of rollsmart.py
    """
    def __init__(self, *args, **kwargs):
        super(RollsmartTest, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    RollsmartTest()


