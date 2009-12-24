##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os.path, doctest, unittest
from zope.testing.doctestunit import DocFileSuite

from z3c.form import testing
from zojax.widget.checkbox import widget


def getPath(filename):
    return os.path.join(os.path.dirname(widget.__file__), filename)


def test_suite():
    return unittest.TestSuite((
        DocFileSuite('tests.txt',
                     setUp=testing.setUp, tearDown=testing.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        DocFileSuite('optcheckbox.txt',
                     setUp=testing.setUp, tearDown=testing.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))
