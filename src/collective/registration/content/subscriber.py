# -*- coding: utf-8 -*-

from collective.registration import _
from datetime import datetime
from plone import schema as ploneschema
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ISubscriber(model.Schema):
    """ Marker interface and Dexterity Python Schema for Subscriber
    """

    first_name = schema.TextLine(title=_(u"First name"), required=True)

    last_name = schema.TextLine(title=_(u"Last name"), required=True)

    email = ploneschema.Email(title=_(u"Email"), required=True)

    number_of_people = schema.Int(title=_(u"Number of people"), required=True)

    subscription_date = schema.Datetime(
        title=_(u"Subscription time"), required=True, default=datetime.now(),
    )

    all_informations = RichText(
        title=_(u"Summary of all other informations"), required=False,
    )


@implementer(ISubscriber)
class Subscriber(Item):
    """
    """
