# -*- coding: utf-8 -*-

from plone import schema as ploneschema
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from collective.registration import _


class ISubscriber(model.Schema):
    """ Marker interface and Dexterity Python Schema for Subscriber
    """

    first_name = schema.TextLine(
        title=_(u'First name'),
        required=True
    )

    last_name = schema.TextLine(
        title=_(u'Last name'),
        required=True
    )

    mail = ploneschema.Email(
        title=_(u'Email'),
        required=True
    )

    number_of_people = schema.Int(
        title=_(u'Number of people'),
        required=True
    )


@implementer(ISubscriber)
class Subscriber(Container):
    """
    """
