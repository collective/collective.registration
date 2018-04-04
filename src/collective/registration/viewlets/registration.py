# encoding: utf-8
from plone import api

from plone.app.layout.viewlets import common as base
from collective.registration.interfaces import IRegistration
from datetime import datetime
from collective.registration.utils import aivability_registration

class RegistrationViewlet(base.ViewletBase):

    def is_authorized(self):
        if IRegistration.providedBy(self.context.aq_parent):
            self.parent = self.context.aq_parent
            return True
        else:
            return False

    def url(self):
        registration = api.content.find(context=self.parent, portal_type='FormFolder')[0]
        return registration.getURL()

    def aivability_registration(self):
        # des périodes dans le future + place disponible
        period_brains = api.content.find(context=self.parent, portal_type='period')
        periods = [period.getObject() for period in period_brains]

        for period in periods:
            if aivability_registration(period):
                return True
        return False
