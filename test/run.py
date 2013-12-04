"""
Runs all tests
"""

import unittest

# -- Import the test modules
from klv_test import TestKLV

# -- Create test suites for each test case module
test_klv_suite = unittest.TestLoader().loadTestsFromTestCase(TestKLV)

# -- Create a single all-encompassing test suite
test_suite = unittest.TestSuite(
    (test_klv_suite,)
)

# -- Set the log level
# logging.basicConfig(level = logging.DEBUG)

# -- Run the tests
unittest.TextTestRunner(verbosity = 2).run(test_suite)