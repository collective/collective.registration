# -*- coding: utf-8 -*-
from zope import schema

from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from collective.registration import _


class IPeriod(model.Schema):
    """ Marker interface and Dexterity Python Schema for Period
    """

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

    nb_place = schema.Int(
        title=_(u'Number of places'),
    )


@implementer(IPeriod)
class Period(Container):
    """
    """
