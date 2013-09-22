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

"""Tests for none_always_valid."""

from __future__ import absolute_import

import sys

import testsuite.testa.modulea

from testsuite.test_all import assert_warnings, pydocchecker


def main():
    instance_a = testsuite.testa.modulea.ClassA()

    # No warnings here, because None is ok.
    testsuite.testa.modulea.foo(instance_a, 0)
    instance_a.bar(instance_a, 0)
    testsuite.testa.modulea.foo(None, 0)
    instance_a.bar(None, 0)
    assert_warnings(0)

    return 0


if __name__ == "__main__":
    pydocchecker.check_all(["testsuite"], none_always_valid=True, debug=5)
    sys.exit(main())
