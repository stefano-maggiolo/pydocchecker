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


def foo_list_1(list_int):
    """Testing list.

    list_int ([int]): a list of integers.

    return ([int]): list_int.

    """
    return list_int
foo_list_1.ok = [
    [1],
    [1, 2, 3],
    [1, 1, 1, 1, 1],
    list(),
    ]
foo_list_1.not_ok = [
    None,
    dict(),
    set(),
    tuple(),
    [None],
    ["1"],
    [1.0],
    1,
    ]


def foo_list_2(list_):
    """Testing list.

    list_ ([]): a list.

    return ([object]): list_ ([] and [object] are synonyms).

    """
    return list_
foo_list_2.ok = [
    [1],
    [1, 2, 3],
    [1, 1, 1, 1, 1],
    list(),
    ]
foo_list_2.not_ok = [
    None,
    set(),
    dict(),
    tuple(),
    1,
    ]


def foo_tuple_1(tuple_two_ints):
    """Testing tuple.

    tuple_two_ints ((int, int)): a tuple of two integers.

    return ((int, int)): tuple_two_ints.

    """
    return tuple_two_ints
foo_tuple_1.ok = [
    (1, 1),
    (-1, 1000000000),
    ]
foo_tuple_1.not_ok = [
    None,
    dict(),
    list(),
    set(),
    tuple(),
    (1, None),
    (None, 1),
    (1,),
    1,
    (1, 1, 1),
    ("1", 1),
    ]


def foo_tuple_2(tuple_int_str):
    """Testing tuple.

    tuple_int_str ((int, str)): a tuple of integer and string.

    return ((int, str)): tuple_int_str.

    """
    return tuple_int_str
foo_tuple_2.ok = [
    (1, "1"),
    (-1, ""),
    ]
foo_tuple_2.not_ok = [
    None,
    dict(),
    list(),
    set(),
    tuple(),
    (1, None),
    (None, "1"),
    (1, 1),
    (1,),
    1,
    (1, "1", 1),
    ("1", 1),
    [1, "1"],
    ]


def foo_tuple_3(tuple_int_str_float):
    """Testing tuple.

    tuple_int_str_float ((int, str, float)): a tuple of integer,
        string, and float.

    return ((int, str, float)): tuple_int_str_float.

    """
    return tuple_int_str_float
foo_tuple_3.ok = [
    (1, "1", 1.0),
    (-1, "", 0.0),
    ]
foo_tuple_3.not_ok = [
    None,
    dict(),
    list(),
    set(),
    tuple(),
    (1, None, 1.0),
    (None, "1", 1.0),
    (1, "1", None),
    (1, "1", 1),
    (1, "1"),
    (1,),
    1,
    (1, "1", 1, 1.0),
    ("1", 1, 1.0),
    [1, "1", 1.0],
    ]


def foo_dict_1(dict_):
    """Testing dict.

    dict_ ({}): a dictionary.

    return ({object: object}): dict_.

    """
    return dict_
foo_dict_1.ok = [
    dict(),
    {1: "a"},
    {1: 1, "2": 2, 2: "2"},
    {None: None},
    ]
foo_dict_1.not_ok = [
    None,
    list(),
    set(),
    tuple(),
    ]


def foo_dict_2(dict_):
    """Testing dict.

    dict_ ({unicode: (int, string)}): a dictionary.

    return ({unicode: (int, string)}): dict_.

    """
    return dict_
foo_dict_2.ok = [
    {u"a": (1, u"b")},
    {u"a": (1, "b")},
    {u"a": (1, "b"), u"b": (-1, "c")},
    dict(),
    ]
foo_dict_2.not_ok = [
    None,
    list(),
    set(),
    tuple(),
    {"a": (1, "b")},
    {u"a": 1},
    {u"a": (1,)},
    ]


def foo_dict_3(dict_):
    """Testing dict.

    dict_ ({keya: (int, string), keyb: unicode}): a dictionary.

    return ({keya: (int, string), keyb: unicode}): dict_.

    """
    return dict_
foo_dict_3.ok = [
    {"keya": (1, u"b"), "keyb": u"b"},
    {"keya": (1, "b"), "keyb": u"b"},
    {u"keya": (1, "b"), u"keyb": u"b"},
    {"keya": (1, "b"), "keyb": u"b", "b": (-1, "c")},
    {"keya": (1, "b"), "keyb": u"b", 2: (-1, "c")},
    {"keya": (1, "b"), "keyb": u"b", None: None},
    ]
foo_dict_3.not_ok = [
    None,
    list(),
    set(),
    tuple(),
    {"keya": (1, "b")},
    {"keyb": "b"},
    dict(),
    ]


def foo_or_1(obj):
    """Testing or.

    obj ([int]|int|None): some object

    return (None|[int]|int): obj.

    """
    return obj
foo_or_1.ok = [
    None,
    list(),
    [1, 2],
    1,
    ]
foo_or_1.not_ok = [
    dict(),
    set(),
    tuple(),
    (1, 2),
    "1"
    ]


def foo_complex_1(obj):
    """Testing complex object.

    obj ([({int: str}, str)]): a complex object.

    return ([({int: str}, str)]): obj.

    """
    return obj
foo_complex_1.ok = [
    list(),
    [({}, "a")],
    [({1: "a", 2: "b"}, "a")],
    [({1: "a", 2: "b"}, "a"), ({}, "b")],
    ]
foo_complex_1.not_ok = [
    None,
    dict(),
    set(),
    tuple(),
    [(1, "a")],
    ]
