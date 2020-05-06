# -*- coding: utf-8 -*-

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.registration


class CollectiveRegistrationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.registration)

    def setUpPloneSite(self, portal):
        installer = portal["portal_quickinstaller"]
        installer.installProduct("collective.registration")
        applyProfile(portal, "collective.registration:default")


COLLECTIVE_REGISTRATION_FIXTURE = CollectiveRegistrationLayer()


COLLECTIVE_REGISTRATION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_REGISTRATION_FIXTURE,),
    name="CollectiveRegistrationLayer:IntegrationTesting",
)


COLLECTIVE_REGISTRATION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_REGISTRATION_FIXTURE,),
    name="CollectiveRegistrationLayer:FunctionalTesting",
)
