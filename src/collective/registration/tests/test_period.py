# -*- coding: utf-8 -*-

from collective.registration.content.period import IPeriod
from collective.registration.testing import COLLECTIVE_REGISTRATION_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PeriodIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_REGISTRATION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="period")
        schema = fti.lookupSchema()
        self.assertEqual(IPeriod, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="period")
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="period")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IPeriod.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        registration = api.content.create(
            container=self.portal, type="registration", id="registration",
        )
        obj = api.content.create(container=registration, type="period", id="period")
        self.assertTrue(IPeriod.providedBy(obj))
