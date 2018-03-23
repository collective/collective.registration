# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.registration -t test_period.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.registration.testing.COLLECTIVE_REGISTRATION_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_period.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a period
  Given a logged-in site administrator
    and an add period form
   When I type 'My Period' into the title field
    and I submit the form
   Then a period with the title 'My Period' has been created

Scenario: As a site administrator I can view a period
  Given a logged-in site administrator
    and a period 'My Period'
   When I go to the period view
   Then I can see the period title 'My Period'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add period form
  Go To  ${PLONE_URL}/++add++period

a period 'My Period'
  Create content  type=period  id=my-period  title=My Period


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the period view
  Go To  ${PLONE_URL}/my-period
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a period with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the period title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
