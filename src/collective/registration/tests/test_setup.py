# -*- coding: utf-8 -*-
"""Setup tests for this package."""

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest

from collective.registration.testing import COLLECTIVE_REGISTRATION_INTEGRATION_TESTING  # noqa


class TestSetup(unittest.TestCase):
    """Test that collective.registration is properly installed."""

    layer = COLLECTIVE_REGISTRATION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.registration is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.registration'))

    def test_browserlayer(self):
        """Test that ICollectiveRegistrationLayer is registered."""
        from collective.registration.interfaces import (
            ICollectiveRegistrationLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveRegistrationLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_REGISTRATION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get(userid=TEST_USER_ID).getRoles()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.registration'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.registration is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.registration'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveRegistrationLayer is removed."""
        from collective.registration.interfaces import \
            ICollectiveRegistrationLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ICollectiveRegistrationLayer,
           utils.registered_layers())
