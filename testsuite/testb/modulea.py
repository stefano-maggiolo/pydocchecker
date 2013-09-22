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

"""Test instance."""

def foo(a, b):
    """foo

    a (testb.modulea.ClassA): a ClassA.
    b (int): a int.

    return (testb.modulea.ClassA): a.

    """
    if b == 0:
        return a
    else:
        return None


class ClassA(object):
    def bar(self, a, b):
        """bar

        a (testb.modulea.ClassA): a ClassA.
        b (int): a int.

        return (testb.modulea.ClassA): a.

        """
        if b == 0:
            return a
        else:
            return None
