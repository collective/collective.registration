# -*- coding: utf-8 -*-

from collective.easyform.actions import DummyFormView
from collective.easyform.api import get_actions
from collective.easyform.api import is_file_data
from collective.easyform.api import OrderedDict
from collective.easyform.browser.view import EasyFormForm
from collective.registration.content.subscriber import ISubscriber
from plone import api
from plone.app.multilingual import api as api_lng
from plone.app.multilingual.interfaces import IPloneAppMultilingualInstalled
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.textfield.value import RichTextValue
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.schema import getFieldsInOrder


class SubscriberView(BrowserView):
    def add_subscriber_in_period(self, context, period, subscriber, form, data):
        request = self.request
        subscriber.first_name = data.get("first_name")
        subscriber.last_name = data.get("last_name")
        subscriber.email = data.get("email")
        subscriber.number_of_people = int(data.get("number_of_people"))
        subscriber.reindexObject()
        period.reindexObject()

        mailer = get_actions(context).get("mailer")
        if not mailer:
            return

        extra_form = DummyFormView(context, request)
        extra_form.schema = form.schema
        extra_form.prefix = "form"
        extra_form._update()
        subscriber_fields = [x[0] for x in getFieldsInOrder(ISubscriber)]
        subscriber_fields.append("period")

        widgets = filter_widgets(extra_form.widgets, subscriber_fields)
        data = filter_fields(data, extra_form.schema, subscriber_fields)
        bodyfield = mailer.body_pt

        extra = {
            "data": data,
            "fields": OrderedDict(
                [(i, j.title) for i, j in getFieldsInOrder(extra_form.schema)],
            ),
            "widgets": widgets,
            "mailer": mailer,
            "body_pre": "",
            "body_post": "",
            "body_footer": "",
        }
        template = ZopePageTemplate(mailer.__name__)
        template.write(bodyfield)
        template = template.__of__(context)
        subscriber.all_informations = RichTextValue(
            template.pt_render(extra_context=extra),
        )
        subscriber.reindexObject()

    def add_subscriber(self, context, fields):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)
        form = EasyFormForm(context, request)
        form.updateFields()
        form.updateWidgets()
        data, errors = form.extractData()

        period_id = data.get("period")
        if isinstance(period_id, list):
            period_id = period_id[0]
        period = context.aq_parent.get(period_id)
        title = "{0} {1}".format(data.get("last_name"), data.get("first_name"))

        subscriber = api.content.create(
            container=period, type="subscriber", title=title,
        )
        self.add_subscriber_in_period(context, period, subscriber, form, data)

        if not IPloneAppMultilingualInstalled.providedBy(request):
            return

        registry = getUtility(IRegistry)
        langs = list(registry["plone.available_languages"])
        current_lang = api.portal.get_current_language()[:2]
        langs.remove(current_lang)

        for lang in langs:
            trans = ITranslationManager(period).get_translation(lang)
            if trans:
                new_subscriber = api_lng.translate(subscriber, lang)
                new_subscriber.title = title
                self.add_subscriber_in_period(
                    context, trans, new_subscriber, form, data,
                )


def filter_fields(data, schema, subscriber_fields):
    data = OrderedDict(
        [(x[0], data[x[0]]) for x in getFieldsInOrder(schema) if x[0] in data],
    )
    fields = [f for f in data if not (is_file_data(data[f]))]
    # remove standard fields (in subscriber schema)
    fields = [f for f in fields if f not in subscriber_fields]
    # remove empties
    fields = [f for f in fields if data[f]]
    ret = OrderedDict([(f, data[f]) for f in fields])
    return ret


def filter_widgets(widgets, subscriber_fields):
    filtered_widgets = {}
    for field_id, widget in widgets.items():
        if field_id not in subscriber_fields:
            filtered_widgets[field_id] = widget.render()
    return filtered_widgets
