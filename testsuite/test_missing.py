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

"""Tests for the usual behavior."""

from __future__ import absolute_import

import sys

import testsuite.testa.modulea
import testsuite.testc.modulea

from testsuite.test_all import assert_warnings, pydocchecker


def main():
    # Warning for missing pydoc and missing argument type when
    # patching the module.
    assert_warnings(2)

    instance_a = testsuite.testa.modulea.ClassA()
    instance_c = testsuite.testc.modulea.ClassA()

    # No warnings here.
    testsuite.testa.modulea.foo(instance_a, 0)
    instance_a.bar(instance_a, 0)
    assert_warnings(0)

    # No further warning for missing pydoc or type information.
    testsuite.testc.modulea.foo(instance_c, 0)
    instance_c.bar(instance_c, 0)
    assert_warnings(0)

    return 0


if __name__ == "__main__":
    pydocchecker.check_all(["testsuite"],
                           complain_for_missing_pydoc=True,
                           debug=True)
    sys.exit(main())
