# -*- coding: utf-8 -*-

from collective.registration.interfaces import IRegistration
from datetime import datetime
from plone import api
from plone.app.multilingual.interfaces import IPloneAppMultilingualInstalled
from plone.app.multilingual.interfaces import ITranslatable
from plone.app.multilingual.interfaces import ITranslationManager
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ILanguage
from zope.component import getUtility


def availability_registration(period_brain):
    if period_brain.end >= datetime.now().date():
        if period_brain.available_places > 0:
            return True
    return False


def link_translations(request, registration):
    if not IPloneAppMultilingualInstalled.providedBy(request):
        return

    if not IRegistration.providedBy(registration):
        return

    if not ITranslatable.providedBy(registration):
        return

    registry = getUtility(IRegistry)
    langs = list(registry["plone.available_languages"])
    current_lang = api.portal.get_current_language()[:2]
    langs.remove(current_lang)

    types = ["EasyForm", "Event"]

    for lang in langs:
        trans_registration = ITranslationManager(registration).get_translation(lang)
        if not trans_registration:
            continue

        for portal_type in types:
            brains = api.content.find(context=registration, portal_type=portal_type)
            if len(brains) != 1:
                continue
            obj = brains[0].getObject()
            if not ITranslatable.providedBy(obj):
                continue
            trans = ITranslationManager(obj).get_translation(lang)
            if trans:
                continue

            trans_brains = api.content.find(
                context=trans_registration, portal_type=portal_type,
            )
            if len(trans_brains) != 1:
                continue

            trans_obj = trans_brains[0].getObject()
            ITranslationManager(obj).register_translation(lang, trans_obj)
            ILanguage(trans_obj).set_language(lang)
