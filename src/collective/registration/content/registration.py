# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.statusmessages.interfaces import IStatusMessage
from plone import api
from plone.dexterity.content import Container
from zope.interface import implementer

from collective.registration import _
from collective.registration.interfaces import IRegistration

SCRIPT = """
## Python Script
##bind container=container
##bind context=context
##bind subpath=traverse_subpath
##parameters=fields, ploneformgen, request
##title=
##
ploneformgen.restrictedTraverse('add_subscriber')(ploneformgen, fields)"""


@implementer(IRegistration)
class Registration(Container):
    """
    """


def create_registration_event(object, event):
    object.REQUEST.RESPONSE.redirect(object.absolute_url() + '/++add++Event?')


def event_add_cancelled_event(object, event):
    url = object.aq_parent.absolute_url()
    messages = IStatusMessage(object.REQUEST)
    messages.add(u"The creation of registration has cancelled", type=u"info")
    api.content.delete(obj=object)
    object.REQUEST.RESPONSE.redirect(url)


def create_event_event(object, event):
    if IRegistration.providedBy(object.aq_parent):
        parent = object.aq_parent
        parent.manage_addProperty('default_page', object.id, 'string')
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
    setattr(form, 'actionAdapter', ())

    form['thank-you'].setShowAll(False)
    form['thank-you'].setDescription(_(u'Thank you for your registration'))
    form['comments'].setRequired(False)

    subscriber_field = api.content.create(
        type='FormCustomScriptAdapter',
        title=_(u'Add subscriber'),
        container=form
    )
    subscriber_field.updateScript(SCRIPT, 'none')

    last_name = api.content.create(
        type='FormStringField',
        title=_(u'Last name'),
        required=True,
        container=form)

    first_name = api.content.create(
        type='FormStringField',
        title=_(u'first name'),
        required=True,
        container=form)

    nb_available_places = api.content.create(
        type='FormIntegerField',
        title=_(u'Number available places'),
        required=True,
        default=0,
        container=form)

    periods = api.content.create(
        type='FormSelectionPeriodField',
        title=_(u'Period field'),
        required=True,
        container=form
    )

    form.moveObjectToPosition(last_name.id, 0)
    form.moveObjectToPosition(first_name.id, 1)
    form.moveObjectToPosition('replyto', 2)
    form.moveObjectToPosition(nb_available_places.id, 3)
