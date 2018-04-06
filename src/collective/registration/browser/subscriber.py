# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api


class SubscriberView(BrowserView):

    def add_subscriber(self, context, fields):
        container = context.getParentNode().get(fields.get('period-field'))

        title = '{0} {1}'.format(fields.get('last-name'), fields.get('first-name'))
        subscriber = api.content.create(
            container=container,
            type='subscriber',
            title=title
        )

        subscriber.last_name = fields.get('last-name')
        subscriber.first_name = fields.get('first_name')
        subscriber.mail = fields.get('replyto')
        subscriber.number_of_persons = int(fields.get('number-available-places'))
        subscriber.reindexObject()

        container.available_place -= int(fields.get('number-available-places'))
