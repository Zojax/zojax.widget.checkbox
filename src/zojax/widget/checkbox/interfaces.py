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


class ICheckboxList(interface.Interface):
    """List with checkbox widget"""


class IOptCheckboxList(ICheckboxList):
    """List with checkbox widget and optional field"""


class ICheckboxWidget(interface.Interface):
    """ checkbox widget """


class IOptCheckboxWidget(ICheckboxWidget):
    """ opt checkbox widget """

    customWidget = interface.Attribute('customWidget')


class ITermItem(interface.Interface):

    id = interface.Attribute('id')
    value = interface.Attribute('value')
    token = interface.Attribute('token')
    title = interface.Attribute('title')
    content = interface.Attribute('content')
    selected = interface.Attribute('selected')
    description = interface.Attribute('description')
