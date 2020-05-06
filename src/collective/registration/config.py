# -*- coding: utf-8 -*-

SUBSCRIPTION_SCRIPT = """
## Python Script
##bind container=container
##bind context=context
##bind subpath=traverse_subpath
##parameters=fields, easyform, request
##title=
##
easyform.restrictedTraverse('add_subscriber')(easyform, fields)
"""


DEFAULT_MAIL_BODY = """
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:tal="http://xml.zope.org/namespaces/tal">
  <head><title></title></head>
  <body>
    <p tal:content="structure body_pre | nothing" />
    <dl>
        <tal:block repeat="field data | nothing">
            <dt tal:content="python:fields[field]" />
            <dd tal:content="structure python:widgets[field]" />
        </tal:block>
    </dl>
    <p tal:content="structure body_post | nothing" />
    <p tal:content="structure body_footer | nothing" />
  </body>
</html>
"""
