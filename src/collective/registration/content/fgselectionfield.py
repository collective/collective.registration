# -*- coding: utf-8 -*-

from Products.PloneFormGen.content.fields import FGSelectionField
from Products.PloneFormGen.content.fieldsBase import BaseFieldSchemaStringDefault
from Products.PloneFormGen.content.fieldsBase import PROJECTNAME
from Products.PloneFormGen.content.fieldsBase import SelectionWidget
from Products.PloneFormGen.content.fieldsBase import StringField
from Products.PloneFormGen.content.fieldsBase import View
from Products.PloneFormGen.content.fieldsBase import registerATCT
from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.schema.vocabulary import SimpleVocabulary

from collective.registration import _
from collective.registration.content.registration import IRegistration
from collective.registration.utils import availability_registration


class FGPeriodSelectionField(FGSelectionField):
    """ Period Selection Field (radio buttons or select) """

    schema = BaseFieldSchemaStringDefault.copy()
    portal_type = meta_type = 'FormPeriodSelectionField'
    archetype_name = 'Period Selection Field'
    content_icon = 'ListField.gif'
    typeDescription = 'Period Selection Field (radio buttons or select)'

    def __init__(self, oid, **kwargs):
        """ initialize class """

        FGSelectionField.__init__(self, oid, **kwargs)

        self.fgField = StringField(
            'PeriodSelectionField',
            required=1,
            widget=SelectionWidget(),
            vocabulary_factory='collective.registration.vocabularies.period',
            write_permission=View,
        )


registerATCT(FGPeriodSelectionField, PROJECTNAME)


def dict_list_2_vocabulary(dict_list):
    """dict_list_2_vocabulary
    Converts a dictionary list to a SimpleVocabulary
    :param dict_list: dictionary list
    """
    terms = []
    for item in dict_list:
        for key in sorted([k for k in item]):
            terms.append(SimpleVocabulary.createTerm(
                key, str(key), item[key]))
    return SimpleVocabulary(terms)


class PeriodVocabularyFactory(object):

    def __call__(self, context):
        registration = context.aq_parent
        values = []
        if IRegistration.providedBy(registration):
            periods = api.content.find(
                context=registration,
                portal_type='period'
            )
            for period in periods:
                obj = period.getObject()
                if not availability_registration(obj):
                    continue
                nb_places_available = obj.available_places
                key = obj.id
                title = obj.title
                start_date = obj.start.strftime('%d/%m/%Y')
                end_date = obj.end.strftime('%d/%m/%Y')
                string = _(u"{0} (from {1} to {2} - {3} place(s) left)")
                value = translate(string,
                                  context=getRequest()).format(
                    title,
                    start_date,
                    end_date,
                    str(nb_places_available)
                )
                item = dict()
                item[key] = value
                values.append(item)

        return dict_list_2_vocabulary(values)


PeriodVocabulary = PeriodVocabularyFactory()
