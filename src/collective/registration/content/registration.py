# -*- coding: utf-8 -*-

from collective.easyform.api import CONTEXT_KEY
from collective.easyform.api import get_actions
from collective.easyform.api import set_actions
from collective.easyform.api import set_fields
from collective.registration import _
from collective.registration.interfaces import IRegistration
from collective.registration.interfaces import IRegistrationActions
from collective.registration.interfaces import IRegistrationForm
from collective.registration.utils import link_translations
from plone import api
from plone.dexterity.content import Container
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer


@implementer(IRegistration)
class Registration(Container):
    """
    """


def create_registration_event(obj, event):
    obj.REQUEST.RESPONSE.redirect(obj.absolute_url() + "/++add++Event?")


def event_add_cancelled_event(obj, event):
    url = obj.aq_parent.absolute_url()
    api.portal.show_message(
        _(u"The creation of registration has been cancelled"),
        request=obj.REQUEST,
        type=u"info",
    )
    api.content.delete(obj=obj)
    obj.REQUEST.RESPONSE.redirect(url)


def create_event_event(obj, event):
    if IRegistration.providedBy(obj.aq_parent):
        parent = obj.aq_parent
        parent.setDefaultPage(obj.id)
        create_registration_form(parent)
        behavior = ISelectableConstrainTypes(parent)
        behavior.setConstrainTypesMode(1)
        behavior.setImmediatelyAddableTypes(("period",))

        request = getattr(event.object, "REQUEST", getRequest())
        link_translations(request, parent)

        url = obj.aq_parent.absolute_url()
        obj.REQUEST.RESPONSE.redirect(url)


def create_registration_form(container):
    current_lang = api.portal.get_current_language()
    reg_text = translate(_(u"Registration to"), target_language=current_lang)

    # Create & configure form
    form = api.content.create(
        type="EasyForm",
        title=u"{0} : {1}".format(reg_text, container.Title()),
        container=container,
    )

    form.exclude_from_nav = True

    set_fields(form, IRegistrationForm)
    form.submitLabel = translate(_(u"Register"), target_language=current_lang)
    form.thankstitle = translate(_(u"Thank you"), target_language=current_lang)
    form.thanksdescription = translate(
        _(u"Thank you for your subscription"), target_language=current_lang,
    )
    form.includeEmpties = False

    # Configure actions
    IRegistrationActions.setTaggedValue(CONTEXT_KEY, form)
    set_actions(form, IRegistrationActions)

    actions = get_actions(form)
    mailer = actions.get("mailer")
    mailer.msg_subject = reg_text

    form.reindexObject()
