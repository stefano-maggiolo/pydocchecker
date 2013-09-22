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

"""Installation for Pydoc Checker."""

from setuptools import setup


setup(name="pydocchecker",
      version="0.1",
      author="Stefano Maggiolo",
      author_email="s.maggiolo@gmail.com",
      url="https://github.com/stefano-maggiolo/pydocchecker",
      download_url="https://github.com/stefano-maggiolo/pydocchecker/"
      "archive/master.tar.gz",
      description="A Python module validating the arguments "
      "of methods and functions.",
      py_modules=["pydocchecker"],
      namespace_packages=[],
      keywords="python type checking validation",
      license="GNU General Public License v3 (GPLv3)",
      zip_safe=True,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Natural Language :: English",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Quality Assurance",
          "License :: OSI Approved :: "
          "GNU General Public License v3 (GPLv3)",
          ],
      test_suite="testsuite.test_all.suite",
      )
