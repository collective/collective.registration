# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IRegistration(model.Schema):
    pass


@implementer(IRegistration)
class Registration(Container):
    """
    """


def create_registration_event(object, event):
    object.REQUEST.RESPONSE.redirect(object.absolute_url() + '/++add++Event?')


def create_event_event(object, event):
    if IRegistration.providedBy(object.aq_parent):
        parent = object.aq_parent
        parent.manage_addProperty('default_page', object.id, 'string')
        behavior = ISelectableConstrainTypes(parent)
        behavior.setConstrainTypesMode(1)
        behavior.setImmediatelyAddableTypes(('period',))
