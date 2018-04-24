# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api
from collective.registration import _


class SubscriberView(BrowserView):

    def add_subscriber(self, context, fields):
        period = context.getParentNode().get(fields.get('period'))

        title = '{0} {1}'.format(
            fields.get('last-name'),
            fields.get('first-name')
        )
        subscriber = api.content.create(
            container=period,
            type='subscriber',
            title=title
        )

        subscriber.first_name = fields.get('first-name')
        subscriber.last_name = fields.get('last-name')
        subscriber.mail = fields.get('replyto')
        subscriber.number_of_people = int(fields.get('number-of-people'))
        subscriber.reindexObject()

        period.available_places -= int(fields.get('number-of-people'))

    def available_places_validator(self, context, request, value):
        registration = context.getParentNode().getParentNode()
        period = registration.get(request.form.get('period'))
        if int(value) <= period.available_places:
            return False
        return _('Not enough places left in the selected period')
