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


_TESTS = [
    "success",
    "none_allowed",
    ]


class PydocCheckerTests(unittest.TestCase):
    def setUp(self):
        pass

    def _test(self, filename):
        assert 0 == os.system(os.path.join(".", "testsuite", filename))


for test in _TESTS:
    setattr(PydocCheckerTests,
            "test_%s" % test,
            lambda self: self._test("test_%s.py" % test))


def suite():
    ret = unittest.TestSuite()
    ret.addTest(unittest.makeSuite(PydocCheckerTests))
    return ret


def main():
    return unittest.TextTestRunner().run(suite())


if __name__ == "__main__":
    sys.exit(not main())
