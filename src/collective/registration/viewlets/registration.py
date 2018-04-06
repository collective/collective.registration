# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.viewlets import common as base

from collective.registration.interfaces import IRegistration
from collective.registration.utils import aivability_registration


class RegistrationViewlet(base.ViewletBase):

    def is_authorized(self):
        if IRegistration.providedBy(self.context.aq_parent):
            self.parent = self.context.aq_parent
            return True
        else:
            return False

    def subscription_url(self):
        subscription = api.content.find(context=self.parent, portal_type='FormFolder')[0]
        return subscription.getURL()

    def period_url(self):
        registration_url = api.content.find(context=self.parent, portal_type='registration')[0].getURL()
        url = "{0}/++add++period".format(registration_url)
        return url

    def aivability_registration(self):
        # des périodes dans le future + place disponible
        period_brains = api.content.find(context=self.parent, portal_type='period')
        periods = [period.getObject() for period in period_brains]

        for period in periods:
            if aivability_registration(period):
                return True
        return False
