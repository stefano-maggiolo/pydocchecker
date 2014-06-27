#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pydoc Checker
# Copyright © 2014 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
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

import sys

import testsuite.teste
from testsuite.teste import bar

from testsuite.test_all import assert_warnings, pydocchecker


def test(func):
    assert '__pydc_patched__' in func.__dict__, \
        "A function was not patched"
    assert func.__pydc_patched__, \
        "A function was not patched"


def main():
    assert id(testsuite.teste.bar) == id(testsuite.teste.modulea.bar), \
        "Patching didn't update a reference"

    test(testsuite.teste.foo)
    test(testsuite.teste.bar)
    test(bar)
    test(testsuite.teste.modulea.bar)

    # bar2 is never directly imported, but since it belongs to modulea
    # which has something imported, then we expect it to be patched.
    test(testsuite.teste.modulea.bar2)


if __name__ == "__main__":
    pydocchecker.check_all(["testsuite"], debug=5)
    sys.exit(main())
