# -*- coding: utf-8 -*-

from collective.registration import _
from collective.registration.interfaces import IRegistration
from plone import api
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IPeriod(model.Schema):
    """ Marker interface and Dexterity Python Schema for Period
    """

    start = schema.Date(title=_(u"Start date"))

    end = schema.Date(title=_(u"End date"))

    nb_places = schema.Int(title=_(u"Number of total available places"))


@implementer(IPeriod)
class Period(Container):
    """
    """


def create_period_event(obj, event):
    url = obj.aq_parent.absolute_url()
    if IRegistration.providedBy(obj.aq_parent):
        obj.REQUEST.RESPONSE.redirect(url)


@indexer(IPeriod)
def available_places(obj):
    brains = api.content.find(context=obj, portal_type="subscriber")
    if not brains:
        return obj.nb_places
    total_people = 0
    for brain in brains:
        if brain.number_of_people:
            total_people += brain.number_of_people
    return obj.nb_places - total_people
