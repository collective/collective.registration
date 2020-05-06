# -*- coding: utf-8 -*-

from collective.easyform import actions
from collective.registration import _
from collective.registration.config import DEFAULT_MAIL_BODY
from collective.registration.config import SUBSCRIPTION_SCRIPT
from plone import schema
from plone.app.textfield.value import RichTextValue
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveRegistrationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRegistration(model.Schema):
    """"""


class IRegistrationForm(model.Schema):
    """"""

    email = schema.Email(title=_(u"Email address"), required=True)

    first_name = schema.TextLine(title=_(u"First name"), required=True)

    last_name = schema.TextLine(title=_(u"Last name"), required=True)

    number_of_people = schema.Int(
        title=_(u"Number of people"), required=True, default=1, min=1,
    )

    period = schema.Choice(
        title=_(u"Period"),
        source="collective.registration.vocabularies.periods",
        required=True,
    )


class IRegistrationActions(model.Schema):
    """"""

    mailer = actions.Mailer(
        title=_(u"Email response"),
        description=_(u"Email based on form inputs"),
        body_pt=DEFAULT_MAIL_BODY,
        to_field=u"email",
        replyto_field=None,
        subject_field=None,
        includeEmpties=False,
        body_pre=RichTextValue(
            _(u"Informations about your subscription"), "text/plain", "text/html",
        ),
    )

    sub_script = actions.CustomScript(
        title=_(u"Subscription adding"),
        ProxyRole="Manager",
        ScriptBody=SUBSCRIPTION_SCRIPT,
    )

    save = actions.SaveData(
        title=_(u"Subscription saving"), UseColumnNames=True, ExtraData=["dt"],
    )
