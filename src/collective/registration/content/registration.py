# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.dexterity.content import Container
from zope.interface import implementer

from collective.registration import _
from collective.registration.interfaces import IRegistration
from Products.TALESField._tales import Expression

SUBSCRIPTION_SCRIPT = """
## Python Script
##bind container=container
##bind context=context
##bind subpath=traverse_subpath
##parameters=fields, ploneformgen, request
##title=
##
ploneformgen.restrictedTraverse('add_subscriber')(ploneformgen, fields)"""

AVAILABLE_PLACES_VALIDATOR = """
python: here.restrictedTraverse('available_places_validator')(here, request, value)
"""


@implementer(IRegistration)
class Registration(Container):
    """
    """


def create_registration_event(obj, event):
    obj.REQUEST.RESPONSE.redirect(obj.absolute_url() + '/++add++Event?')


def event_add_cancelled_event(obj, event):
    url = obj.aq_parent.absolute_url()
    api.portal.show_message(
        _(u"The creation of registration has been cancelled"),
        request=obj.REQUEST,
        type=u"info"
    )
    api.content.delete(obj=obj)
    obj.REQUEST.RESPONSE.redirect(url)


def create_event_event(obj, event):
    if IRegistration.providedBy(obj.aq_parent):
        parent = obj.aq_parent
        parent.manage_addProperty('default_page', obj.id, 'string')
        create_registration_form(parent)
        behavior = ISelectableConstrainTypes(parent)
        behavior.setConstrainTypesMode(1)
        behavior.setImmediatelyAddableTypes(('period',))


def create_registration_form(portal):
    form = api.content.create(
        type='FormFolder',
        title='Registration',
        container=portal)
    api.content.delete(obj=form['topic'])

    form['thank-you'].setShowAll(False)
    form['thank-you'].setDescription(_(u'Thank you for your subscription'))
    form['comments'].setRequired(False)
    form.setExcludeFromNav(1)
    form['mailer'].setMsg_subject(_(u'Confirmation of your subscription'))
    form['mailer'].setBody_pre(_(u'Informations about your subscription'))
    form['mailer'].setTo_field('replyto')
    subscriber_field = api.content.create(
        type='FormCustomScriptAdapter',
        title=_(u'Add subscriber'),
        container=form
    )
    subscriber_field.updateScript(SUBSCRIPTION_SCRIPT, 'none')

    first_name = api.content.create(
        type='FormStringField',
        title=_(u'First name'),
        required=True,
        container=form)

    last_name = api.content.create(
        type='FormStringField',
        title=_(u'Last name'),
        required=True,
        container=form)

    nb_people = api.content.create(
        type='FormIntegerField',
        title=_(u'Number of people'),
        required=True,
        default=0,
        container=form)
    value = Expression.Expression(AVAILABLE_PLACES_VALIDATOR)
    nb_people.fgTValidator = value

    period = api.content.create(
        type='FormPeriodSelectionField',
        title=_(u'Period'),
        required=True,
        container=form
    )

    api.content.create(
        type='FormSaveDataAdapter',
        title=_(u'CSV'),
        required=True,
        container=form
    )

    form.moveObjectToPosition(period.id, 0)
    form.moveObjectToPosition(first_name.id, 1)
    form.moveObjectToPosition(last_name.id, 2)
    form.moveObjectToPosition('replyto', 3)
    form.moveObjectToPosition(nb_people.id, 4)
