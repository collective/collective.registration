# -*- coding: utf-8 -*-

from collective.registration import _
from collective.registration.content.registration import IRegistration
from collective.registration.utils import availability_registration
from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.schema.vocabulary import SimpleVocabulary


def dict_list_2_vocabulary(dict_list):
    """dict_list_2_vocabulary
    Converts a dictionary list to a SimpleVocabulary
    :param dict_list: dictionary list
    """
    terms = []
    for item in dict_list:
        for key in sorted([k for k in item]):
            terms.append(SimpleVocabulary.createTerm(key, str(key), item[key]))
    return SimpleVocabulary(terms)


class PeriodsVocabularyFactory(object):
    def __call__(self, context):
        if isinstance(context, dict):
            return SimpleVocabulary([])
        registration = context.aq_parent
        values = []
        if IRegistration.providedBy(registration):
            brains = api.content.find(context=registration, portal_type="period")
            for brain in brains:
                if not availability_registration(brain):
                    continue
                nb_places_available = brain.available_places
                key = brain.getId
                title = brain.Title
                start_date = brain.start.strftime("%d/%m/%Y")
                end_date = brain.end.strftime("%d/%m/%Y")
                string = _(u"{0} (from {1} to {2} - {3} place(s) left)")
                value = translate(string, context=getRequest()).format(
                    title.decode("utf-8"),
                    start_date,
                    end_date,
                    str(nb_places_available),
                )
                item = dict()
                item[key] = value
                values.append(item)

        return dict_list_2_vocabulary(values)


PeriodsVocabulary = PeriodsVocabularyFactory()
