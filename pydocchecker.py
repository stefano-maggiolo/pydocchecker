#!/usr/bin/env python2
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

"""A Python module validating the arguments of methods and functions.

"""

from __future__ import absolute_import

import inspect
import q
import re
import sys
import traceback
import types

from functools import wraps
from warnings import warn


__version__ = "0.1"
__author__ = "Stefano Maggiolo <s.maggiolo@gmail.com>"


# Resolves custom type names to a list of accepted types.
TYPES = {
    "function": [types.FunctionType, types.MethodType],
    "string": [basestring],
    "None": [types.NoneType],
    }


# Configuration, see check_all() for details.
NONE_ALWAYS_VALID = False
COMPLAIN_FOR_MISSING_PYDOC = False
DEBUG = 0


BRACKETS = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">",
    }


def _log(msg, level=5):
    """Log msg with q, if debug is enabled.

    msg (unicode): the message to log

    level (int): the minimum level DEBUG needs to be set in order for
        this message to be logged. Levels are so organized: do not log
        anything (0); log the same message that are issued as warnings
        (1); additional info in case of warnings (2); not used (3);
        log missing pydoc or type information (4); log all patched
        functions and found types (5).

    """
    if DEBUG >= level:
        q / msg


def _warn(msg):
    """Issue a warning and if necessary, log.

    msg (unicode): the string to log.

    """
    warn(msg)
    _log(msg, level=1)


def _describe_function(func):
    """Return the name of the function or method.

    func (function): the function.
    return (unicode): the name of the function.

    """
    name = func.__name__
    if hasattr(func, "im_class"):
        name = "%s.%s" % (func.im_class.__name__, name)
    return name


def _find_closing_bracket(string, index):
    """Return the index of the bracket matching the one at index.

    string (unicode): the string to analyze.
    index (int): the index in string of the open bracket to match.

    return (int): the index in string of the matching bracket.

    raise (ValueError): if the brackets are not well matched, or if
        index is invalid.

    """
    bracket_error = ValueError("Brackets not well matched.")
    if not 0 <= index < len(string) or string[index] not in BRACKETS:
        raise ValueError("Invalid index.")
    waiting_for = BRACKETS[string[index]]
    cur = index + 1
    depth = []
    while cur < len(string):
        char = string[cur]
        if char in BRACKETS:
            depth.append(BRACKETS[char])
        elif char in BRACKETS.values():
            if len(depth) == 0:
                if char == waiting_for:
                    return cur
                else:
                    raise bracket_error
            else:
                if char == depth[-1]:
                    depth = depth[:-1]
                else:
                    raise bracket_error
        cur += 1
    raise bracket_error


def _smart_split(string, char):
    """Split string in correspondence of char, considering brackets.

    This functions splits string at char, when it occurres at depth
    zero, i.e. when it is not inside a bracket. Tokens composed only
    of whitespaced will not be included in the output.

    string (unicode): the string to analyze.
    char (unicode): the char to split at.

    return ([unicode]): the splitted string.

    raise (ValueError): when char is not of length one.

    """
    if len(char) != 1:
        raise ValueError("char must be of length one.")
    depth = 0
    ret = []
    prev = -1
    for idx, cur in enumerate(string):
        if cur in BRACKETS:  # Opening brackets
            depth += 1
        elif cur in BRACKETS.values():  # Closing brackets.
            depth -= 1
        elif cur == char:
            if depth == 0:
                to_append = string[prev + 1:idx].strip()
                if to_append != "":
                    ret.append(to_append)
                prev = idx
    to_append = string[prev + 1:].strip()
    if to_append != "":
        ret.append(to_append)
    return ret


def _check(type_):
    """Return a function checking that an object is of a certain type.

    type_ (unicode): the name of the type to resolve.

    return (function): a function accepting an object and returning
        True if the object is of type type_, and False otherwise.

    raise (ValueError): if the type description is invalid (does not
        parse).

    """
    type_ = type_.strip()

    if type_ == "":
        return lambda x: True

    or_splits = _smart_split(type_, "|")
    if len(or_splits) > 1:
        return lambda obj: \
            any(_check(or_split)(obj)
                for or_split in or_splits)

    if type_[0] in BRACKETS:
        end = _find_closing_bracket(type_, 0)
        if end != len(type_) - 1:
            raise ValueError("Syntax error in type `%s'." % type_)

        if type_[0] == "[":

            def check_list(obj):
                """Check that obj is a valid list."""
                if obj is None:
                    return NONE_ALWAYS_VALID
                if not isinstance(obj, list):
                    return False
                for item in obj:
                    if not _check(type_[1:-1])(item):
                        return False
                return True

            return check_list

        elif type_[0] == "(":
            items_type = _smart_split(type_[1:-1], ",")

            def check_tuple(obj):
                """Check that obj is a valid tuple."""
                if obj is None:
                    return NONE_ALWAYS_VALID
                if not isinstance(obj, tuple):
                    return False
                if len(items_type) != len(obj):
                    return False
                for item, item_type in zip(obj, items_type):
                    if not _check(item_type)(item):
                        return False
                return True

            return check_tuple

        elif type_[0] == "<":

            def check_set(obj):
                """Check that obj is a valid set."""
                if obj is None:
                    return NONE_ALWAYS_VALID
                if not isinstance(obj, set):
                    return False
                for item in obj:
                    if not _check(type_[1:-1])(item):
                        return False
                return True

            return check_set

        else:  # type_[0] == "{"
            keyvalues = [_smart_split(keyvalue, ":")
                         for keyvalue in _smart_split(type_[1:-1], ",")]
            # Heuristic: if there is only one key-value, we assume it
            # is of the form "{type_of_key: type_of_value}";
            # otherwise, of the form "{name_of_key: type_of_value,
            # ...}".
            if len(keyvalues) == 1:

                def check_dict(obj):
                    """Check that obj is a valid dict."""
                    if obj is None:
                        return NONE_ALWAYS_VALID
                    if not isinstance(obj, dict):
                        return False
                    key_type, value_type = keyvalues[0]
                    for key, value in obj:
                        if not _check(key_type)(key):
                            return False
                        if not _check(value_type)(value):
                            return False
                    return True

            else:

                def check_dict(obj):
                    """Check that obj is a valid dict."""
                    if obj is None:
                        return NONE_ALWAYS_VALID
                    if not isinstance(obj, dict):
                        return False
                    for key, value in keyvalues:
                        if key not in obj:
                            return False
                        if not _check(value)(obj[key]):
                            return False
                    return True

            return check_dict
    else:
        # Simple type.
        if type_ in TYPES:

            def check_known_type(obj):
                """Check that obj is a valid known type."""
                if obj is None:
                    return NONE_ALWAYS_VALID
                return any(isinstance(obj, test_type)
                           for test_type in TYPES[type_])

            return check_known_type
        else:
            try:
                # Otherwise try to evaluate the string.
                real_type = eval(type_)
            except Exception:
                # Should be just NameError, but we try to be more
                # conservative given the eval.
                return lambda obj: True
            else:
                # eval succeeded, testing with resulting type.
                return lambda obj: (obj is None and NONE_ALWAYS_VALID) \
                    or isinstance(obj, real_type)


def _check_type(fname, type_, value, name):
    """Check that the value is of the given type.

    If the types do not match, a warning is logged.

    fname (unicode): the name of the function/method.
    type_ (unicode): the name of the type.
    value (object): the value to check.
    name (unicode): the name of the argument to check.

    """
    if type_ is None:
        # No information in the pydoc about this argument.
        return

    checker = _check(type_)
    if checker is None:
        _warn("Not found: %s in %s" % (type_, fname))
    elif not checker(value):
        msg1 = "`%s' received value with wrong type for argument `%r'." % (
            fname, name)
        msg2 = "Value passed: `%r', of type `%r'." % (
            value, value.__class__.__name__)
        msg3 = "Expected type: `%r'." % type_
        _warn("%s\n%s\n%s" % (msg1, msg2, msg3))
        for line in traceback.extract_stack():
            _log(line, level=2)


def _extract_expected_type(doc, name):
    """Try to extract the extected type of an argument from the pydoc.

    doc__ (unicode): the pydoc of the function.
    name__ (unicode): the name of an argument.

    return (unicode): the name of the expected type of the argument,
        or None if could not extract.

    """
    type_ = None
    ret = re.search(r"\n\n(.*\n)*%s \(([^:]*)\):" % name, doc)
    if ret is not None:
        try:
            type_ = ret.groups()[-1]
        except IndexError:
            # Cannot decode format.
            pass
    return type_


def _decorate_function(func):
    """Decorates the function to check for arguments' types.

    func (function): the function to decorate.
    return (function): the decorated function.

    """
    fname = _describe_function(func)
    _log("Patching function `%s'." % fname, level=5)

    # If there is no pydoc, then there is nothing to do.
    doc = inspect.getdoc(func)
    if doc is None:
        msg = "Missing pydoc for `%s'." % fname
        if COMPLAIN_FOR_MISSING_PYDOC:
            _warn(msg)
        else:
            _log(msg, level=4)
        return func

    # Retrieve arguments data.
    try:
        arg_names, _, _, defaults = inspect.getargspec(func)
    except TypeError:
        # Maybe it's not Python code; in that case, do nothing.
        return func
    # defaults refers to the last len(defaults) arguments.
    if defaults is None:
        defaults = []
    displacement = len(arg_names) - len(defaults)

    arg_types = []
    for i, name in enumerate(arg_names):
        # Try to get the expected type from the pydoc.
        type_ = _extract_expected_type(doc, name)
        # If the type is not specified (and this is not the first
        # argument of a method), maybe warn.
        if type_ is None and (name != "self" or i != 0):
            msg = "Missing type information for argument `%s' in `%s'." % (
                name, fname)
            if COMPLAIN_FOR_MISSING_PYDOC:
                _warn(msg)
            else:
                _log(msg, level=4)
        arg_types.append(type_)
        # If the argument has a default value, check its type.
        if i - displacement >= 0:
            _check_type(fname, type_, defaults[i - displacement], name)

    # Install the checker also for the return value.
    ret_type = _extract_expected_type(doc, "return")
    if ret_type is None:
        ret_type = _extract_expected_type(doc, "returns")

    @wraps(func)
    def internal(*args, **kwargs):
        """Decorated function."""
        for i, name in enumerate(arg_names):
            if i < len(args):
                _check_type(fname, arg_types[i], args[i], name)
            elif name in kwargs:
                _check_type(fname, arg_types[i], kwargs[name], name)
        ret_value = func(*args, **kwargs)
        _check_type(fname, ret_type, ret_value, "__return__")
        return ret_value

    return internal


def _decorate_class(cls):
    """Decorates all the methods in cls.

    cls (type): the class whose methods need to be decorated.

    return (type): the class with the method decorated.

    """
    _log("Patching class %s." % cls.__name__, level=5)
    for key, value in cls.__dict__.iteritems():
        if callable(value):
            setattr(cls, key, _decorate_function(getattr(cls, key)))
    return cls


def _to_be_checked(package, packages):
    """Return true if package is (a subpackage of) one in packages.

    package (unicode): the name of the package to maybe decorate.
    packages ([unicode]): the list of requested packages to decorate.

    return (bool): True if package is in packages, or is a subpackage
        of a package in packages.

    """
    package_split = package.split(".")
    for pkg in packages:
        pkg_split = pkg.split(".")
        length = len(pkg_split)
        if length <= len(package_split):
            if package_split[:length] == pkg_split:
                return True
    return False


def _decorate_packages(packages):
    """Decorate with type checking all requested packages.

    packages ([unicode]): list of packages to decorate (including
        subpackages).

    """
    for name, module in sys.modules.iteritems():
        if module is None:
            continue
        if not _to_be_checked(name, packages):
            continue
        to_add = {}
        for key, value in module.__dict__.iteritems():
            if not hasattr(value, "__module__") or \
                    value.__module__ != name:
                continue
            if isinstance(value, type):
                to_add[key] = _decorate_class(value)
            elif isinstance(value, types.FunctionType):
                if name == __name__:
                    continue
                to_add[key] = _decorate_function(value)
        module.__dict__.update(to_add)


def _install_test_types():
    """Add to the known types all modules.

    """
    for name, module in sys.modules.iteritems():
        if module is None:
            continue
        name_parts = name.split(".")
        for key, value in module.__dict__.iteritems():
            if not hasattr(value, "__module__") or \
                    value.__module__ != name:
                continue
            if isinstance(value, type):
                for i in xrange(len(name_parts) + 1):
                    complete_name = ".".join(name_parts[i:] + [key])
                    if complete_name not in TYPES:
                        TYPES[complete_name] = []
                    _log("Adding type %s." % complete_name, level=5)
                    TYPES[complete_name].append(value)


def check_all(packages,
              none_always_valid=False,
              complain_for_missing_pydoc=False,
              debug=0):
    """Install the checker on all cms hierarchy.

    To be called at the main, it adds to the known types all cms
    hierarchy, and decorates all methods and functions to check for
    the passed types.

    packages ([unicode]): the list of packages where to install the
        checkers; all subpackages will be checked too.
    none_always_valid (bool): whether to consider None an instance of
        any type, instead then just of object and NoneType. In the
        latter case, use an annotation like <type>|None to accept also
        None values.
    complain_for_missing_pydoc (bool): whether to log a warning also
        for missing pydocs, or missing type descriptions.
    debug (int): the higher, the more log lines will be printed; valid
        values are between 0 and 5.

    """
    global NONE_ALWAYS_VALID, COMPLAIN_FOR_MISSING_PYDOC, DEBUG
    NONE_ALWAYS_VALID = none_always_valid
    COMPLAIN_FOR_MISSING_PYDOC = complain_for_missing_pydoc
    DEBUG = debug

    _install_test_types()
    _decorate_packages(packages)
