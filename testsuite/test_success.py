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
import testsuite.testb.modulea


n_warns = 0  # pylint: disable=C0103


def main():
    instance_a = testsuite.testa.modulea.ClassA()
    instance_b = testsuite.testb.modulea.ClassA()

    # No warnings here.
    testsuite.testa.modulea.foo(instance_a, 0)
    testsuite.testb.modulea.foo(instance_b, 0)
    instance_a.bar(instance_a, 0)
    instance_b.bar(instance_b, 0)
    assert n_warns == 0

    # Wrong first parameter and return value.
    testsuite.testa.modulea.foo(instance_b, 0)
    assert n_warns == 2

    # Wrong first parameter and return value.
    testsuite.testb.modulea.foo(instance_a, 0)
    assert n_warns == 4

    # Wrong first parameter and return value.
    instance_a.bar(instance_b, 0)
    assert n_warns == 6

    # Wrong first parameter and return value.
    instance_b.bar(instance_a, 0)
    assert n_warns == 8

    # Wrong second parameter and return value.
    instance_a.bar(instance_a, "0")
    assert n_warns == 10

    # Wrong first parameter and return value.
    instance_a.bar(None, 0)
    assert n_warns == 12

    # Wrong return value.
    instance_a.bar(instance_a, 1)
    assert n_warns == 13

    return 0


if __name__ == "__main__":
    import pydocchecker
    pydocchecker.check_all(["testsuite"], debug=True)

    def my_warn(_):
        global n_warns
        n_warns += 1
    pydocchecker.warn = my_warn

    sys.exit(main())
