# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model


class ICollectiveRegistrationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRegistration(model.Schema):
    pass
