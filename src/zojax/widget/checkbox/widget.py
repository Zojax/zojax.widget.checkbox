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
from zope.i18n import translate
from zope import interface, component
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.component import getMultiAdapter, queryMultiAdapter

from z3c.form.browser import widget
from z3c.form import converter
from z3c.form.widget import SequenceWidget, FieldWidget
from z3c.form.interfaces import IFormLayer, IFieldWidget, NOVALUE, IDataConverter

from zojax.widget.list.widget import ListFieldWidget
from zojax.layout.interfaces import IPagelet

from interfaces import ITermItem, ICheckboxList, IOptCheckboxList, \
                       ICheckboxWidget, IOptCheckboxWidget


class TermItem(object):
    interface.implements(ITermItem)

    def __init__(self, id, value, token, title, content, selected, description):
        self.id = id
        self.value = value
        self.token = token
        self.title = title
        self.content = content
        self.selected = selected
        self.description = description


class CheckboxWidget(widget.HTMLInputWidget, SequenceWidget):
    interface.implements(ICheckboxWidget)

    items = ()
    klass = u'z-listing'

    def update(self):
        super(CheckboxWidget, self).update()

        if getattr(self.field, 'horizontal', False):
            self.klass = 'z-hlisting'

        widget.addFieldClass(self)

        self.items = []

        for count, term in enumerate(self.terms):
            selected = term.token in self.value
            id = '%s-%i' % (self.id, count)
            content = term.token
            if ITitledTokenizedTerm.providedBy(term):
                content = translate(
                    term.title, context=self.request, default=term.title)

            item = TermItem(id, term.value, term.token, term.title,
                            content, selected, getattr(term, 'description', u''))

            context = getattr(self.form, 'context', None)
            view = queryMultiAdapter(
                (context, self.form,
                 self, item, self.request), IPagelet, term.token)
            if view is None:
                view = getMultiAdapter(
                    (context, self.form, self, item, self.request), IPagelet)

            view.update()
            self.items.append(view)


@interface.implementer(IFieldWidget)
@component.adapter(ICheckboxList, IFormLayer)
def CheckboxWidgetFactory(field, request):
    return FieldWidget(field, CheckboxWidget(request))


class OptCheckboxWidget(CheckboxWidget):
    interface.implements(IOptCheckboxWidget)

    customWidget = None

    def update(self):
        if IFieldWidget.providedBy(self):
            # Clone field again, because we change the ``require`` options
            clone = self.field.bind(self.field.context)
            clone.required = False
            clone.value_type.required = False
            clone.value_type.value_type.required = False
            # Setup the custom value widget
            clone.value_type = clone.value_type.value_type
            clone.value_type.__name__ = 'custom'
            self.customWidget = ListFieldWidget(clone, self.request)

        super(OptCheckboxWidget, self).update()

        if IFieldWidget.providedBy(self):
            tokens = [term.token for term in self.terms]
            self.customWidget.value = IDataConverter(
                self.customWidget).toWidgetValue(
                [value for value in self.value if value not in tokens])

    def extract(self, default=NOVALUE):
        """See z3c.form.interfaces.IWidget."""
        value = super(OptCheckboxWidget, self).extract(default)

        if IFieldWidget.providedBy(self):
            optValue = self.customWidget.extract(default)
            if optValue != default:
                optValue = IDataConverter(self.customWidget).toFieldValue(
                    optValue)
                if value != default:
                    return list(optValue) + value
                return list(optValue)

        return value


class OptCheckboxDataConverter(converter.CollectionSequenceDataConverter):
    """Converter"""

    component.adapts(ICheckboxList, OptCheckboxWidget)

    def toWidgetValue(self, value):
        """Convert from Python bool to HTML representation."""
        widget = self.widget
        if widget.terms is None:
            widget.updateTerms()
        res = []
        for entry in value:
            try:
                res.append(widget.terms.getTerm(entry).token)
            except LookupError:
                res.append(entry)
        return res

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        widget = self.widget
        if widget.terms is None:
            widget.updateTerms()
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        res = []
        for token in value:
            try:
                res.append(widget.terms.getValue(token))
            except LookupError:
                res.append(token)
        return collectionType(res)


@interface.implementer(IFieldWidget)
@component.adapter(IOptCheckboxList, IFormLayer)
def OptCheckboxWidgetFactory(field, request):
    return FieldWidget(field, OptCheckboxWidget(request))
