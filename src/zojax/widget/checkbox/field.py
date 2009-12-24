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
from zope import interface
from zope.schema import List, Choice
from z3c.schema.optchoice.field import OptionalChoice

from zojax.widget.checkbox.interfaces import ICheckboxList, IOptCheckboxList


class CheckboxList(List):
    interface.implements(ICheckboxList)

    def __init__(self, vocabulary=None, horizontal=False, **kw):
        self.horizontal = horizontal
        kw['value_type'] = Choice(vocabulary=vocabulary)

        super(CheckboxList, self).__init__(**kw)


class OptCheckboxList(List):
    interface.implements(IOptCheckboxList)

    def __init__(self, value_type, vocabulary=None, horizontal=False, **kw):
        self.horizontal = horizontal
        kw['value_type'] = OptionalChoice(value_type, vocabulary=vocabulary)

        super(OptCheckboxList, self).__init__(**kw)
