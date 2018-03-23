# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from collective.registration import _


class IPeriod(model.Schema):
    """ Marker interface and Dexterity Python Schema for Period
    """

    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Session title'),
    )

    description = schema.Text(
        title=_(u'Description'),
    )

    details = RichText(
        title=_(u'Details'),
        required=False
    )

    start = schema.Date(
        title=_(u'Start date'),
    )

    end = schema.Date(
        title=_(u'end date'),
    )



@implementer(IPeriod)
class Period(Container):
    """
    """
