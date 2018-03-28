# encoding: utf-8
from Products.PloneFormGen.content.fields import FGSelectionField
from Products.PloneFormGen.content.fieldsBase import BaseFieldSchemaStringDefault
from Products.PloneFormGen.content.fieldsBase import PROJECTNAME
from Products.PloneFormGen.content.fieldsBase import SelectionWidget
from Products.PloneFormGen.content.fieldsBase import StringField
from Products.PloneFormGen.content.fieldsBase import View
from Products.PloneFormGen.content.fieldsBase import registerATCT
from plone import api
from zope.schema.vocabulary import SimpleVocabulary

from collective.registration import _
from collective.registration.content.registration import IRegistration


class FGSelectionPeriodField(FGSelectionField):
    """ Selection Field (radio buttons or select) """

    schema = BaseFieldSchemaStringDefault.copy()
    portal_type = meta_type = 'FormSelectionPeriodField'
    archetype_name = 'Selection Period Field'
    content_icon = 'ListField.gif'
    typeDescription = 'Selection Period Field (radio buttons or select)'

    def __init__(self, oid, **kwargs):
        """ initialize class """

        FGSelectionField.__init__(self, oid, **kwargs)

        self.fgField = StringField(
            'SelectionPeriodField',
            required=1,
            widget=SelectionWidget(),
            vocabulary_factory='collective.registration.vocabularies.period',
            write_permission=View,
        )


registerATCT(FGSelectionPeriodField, PROJECTNAME)


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
            periods = api.content.find(context=registration, portal_type='period')
            for period in periods:
                obj = period.getObject()
                key = obj.id
                title = obj.title
                start_date = obj.start.strftime('%d/%m/%Y')
                end_date = obj.end.strftime('%d/%m/%Y')
                value = _("{0} du {1} au {2}".format(title, start_date, end_date))
                item = dict()
                item[key] = value
                values.append(item)
                print

        return dict_list_2_vocabulary(values)


PeriodVocabulary = PeriodVocabularyFactory()
