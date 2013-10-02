#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pydoc Checker
# Copyright © 2013 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Complete tests for Pydoc Checker."""

import os
import sys
import unittest

import pydocchecker


_TESTS = [
    "success",
    "none_allowed",
    "missing",
    ]


class PydocCheckerTests(unittest.TestCase):
    def setUp(self):
        pass

    def _test(self, filename):
        assert 0 == os.system(os.path.join(".", "testsuite", filename))


# Add all tests.
for test in _TESTS:
    setattr(PydocCheckerTests,
            "test_%s" % test,
            lambda self: self._test("test_%s.py" % test))


def suite():
    """Create the testsuite comprising all the tests."""
    ret = unittest.TestSuite()
    ret.addTest(unittest.makeSuite(PydocCheckerTests))
    return ret


def main():
    """Run all the tests."""
    return unittest.TextTestRunner().run(suite())


def my_warn(_):
    """Custom implementation of warn() for testing."""
    if not hasattr(assert_warnings, "raised_warns"):
        assert_warnings.raised_warns = 0
    assert_warnings.raised_warns += 1


def assert_warnings(expected):
    """Assert that there has been the right amount of warnings.

    expected (int): the expected number of warnings from the last call
        to assert_warnings.

    """
    if not hasattr(assert_warnings, "found_warns"):
        assert_warnings.found_warns = 0
    if not hasattr(assert_warnings, "raised_warns"):
        assert_warnings.raised_warns = 0
    found_now = assert_warnings.raised_warns - assert_warnings.found_warns
    assert expected == found_now, \
        "Expected %d warnings, %d found." % (expected, found_now)
    assert_warnings.found_warns = assert_warnings.raised_warns


# Substitute the warning implementation with a custom one recording
# the number of warnings issued. We need to do so because warnings are
# silently ignored if more arrive from the same code location, but we
# need to catch them all.
pydocchecker.warn = my_warn


if __name__ == "__main__":
    sys.exit(not main())
