# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent

from collective.registration import _
from collective.registration.interfaces import IRegistration


class IPeriod(model.Schema):
    """ Marker interface and Dexterity Python Schema for Period
    """

    start = schema.Date(
        title=_(u'Start date'),
    )

    end = schema.Date(
        title=_(u'End date'),
    )

    nb_places = schema.Int(
        title=_(u'Number of available places'),
    )


@implementer(IPeriod)
class Period(Container):
    """
    """


def create_period_event(obj, event):
    if type(event) == ObjectModifiedEvent:
        if len(event.descriptions) > 0:
            obj.available_places = obj.nb_places
    else:
        obj.available_places = obj.nb_places
        url = obj.aq_parent.absolute_url()
        if IRegistration.providedBy(obj.aq_parent):
            obj.REQUEST.RESPONSE.redirect(url)
