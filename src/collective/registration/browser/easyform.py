# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from collective.easyform.api import get_actions
from plone import api


class EasyFormView(BrowserView):
    def download_csv(self):
        brain = api.content.find(context=self.context, portal_type="EasyForm")[0]
        subscription = brain.getObject()

        savedata = get_actions(subscription).get("save")
        if not savedata:
            return
        return savedata.download_csv(self.request.response)
