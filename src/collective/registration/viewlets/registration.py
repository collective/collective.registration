# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.viewlets import common as base

from collective.registration.interfaces import IRegistration
from collective.registration.utils import availability_registration


class RegistrationViewlet(base.ViewletBase):

    def available(self):
        if IRegistration.providedBy(self.context.aq_parent):
            self.parent = self.context.aq_parent
            return True
        else:
            return False

    def subscription_url(self):
        subscription = api.content.find(
            context=self.parent,
            portal_type='FormFolder'
        )[0]
        return subscription.getURL()

    def period_url(self):
        registration_url = api.content.find(
            context=self.parent,
            portal_type='registration'
        )[0].getURL()
        url = "{0}/++add++period".format(registration_url)
        return url

    def availability_registration(self):
        period_brains = api.content.find(
            context=self.parent,
            portal_type='period'
        )
        periods = [period.getObject() for period in period_brains]

        for period in periods:
            if availability_registration(period):
                return True
        return False

    def can_view_subcriber_list(self):
        current = api.user.get_current()
        if api.user.has_permission('Edit', username=current.getUserName()):
            return True
        return False

    def csv_url(self):
        registration_url = api.content.find(
            context=self.parent,
            portal_type='FormFolder'
        )[0].getURL()
        url = "{0}/csv/download".format(registration_url)
        return url
