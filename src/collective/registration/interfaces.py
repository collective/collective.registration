# -*- coding: utf-8 -*-

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model


class ICollectiveRegistrationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRegistration(model.Schema):
    """"""
