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
        title=_(u'end date'),
    )

    nb_place = schema.Int(
        title=_(u'Number of places'),
    )


@implementer(IPeriod)
class Period(Container):
    """
    """


def create_period_event(object, event):
    if type(event) == ObjectModifiedEvent:
        if len(event.descriptions) > 0:
            object.available_place = object.nb_place
    else:
        object.available_place = object.nb_place
        if IRegistration.providedBy(object.aq_parent):
            registration = object.aq_parent
            object.REQUEST.RESPONSE.redirect(registration.absolute_url())
