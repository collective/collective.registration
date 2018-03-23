# -*- coding: utf-8 -*-
from plone.supermodel import model
from zope.interface import implementer
from plone.dexterity.content import Container


class IRegistration(model.Schema):
    pass


@implementer(IRegistration)
class Registration(Container):
    """
    """
