# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.registration:uninstall',
        ]


def post_install(context):
    """Post install script"""
    from plone import api
    site = api.portal.get()

    ptt = getToolByName(site, 'portal_types')
    allowed_content_types = ptt.getTypeInfo('FormFolder').allowed_content_types
    allowed_content_types += ('FormPeriodSelectionField',)
    ptt.getTypeInfo('FormFolder').manage_changeProperties(
        allowed_content_types=allowed_content_types,
    )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
