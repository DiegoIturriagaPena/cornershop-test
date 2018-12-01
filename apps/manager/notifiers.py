"""Module containing notification functions by mail and by slack."""

from django.conf import settings
from slackclient import SlackClient

from apps.commons import helpers
from apps.employees import helpers as helpers_empl


def send_email_notification(uuid_notification):
    """Email notification."""
    context = {
        'uuid': uuid_notification,
    }
    subject = "Cornershop's Backend Test"
    to_mail = helpers_empl.get_employee_emails()
    html_template = 'layout/template_email.html'
    helpers.email(context, subject, to_mail, html_template)


def send_slack_notification(uuid_notification):
    """Slack notification."""
    slack_token = settings.SLACK_TOKEN
    sc = SlackClient(slack_token)
    message = "Check the menu of day: " \
              "https://nora.cornershop.io/menu/%s" % uuid_notification
    sc.api_call(
        'chat.postMessage',
        channel=settings.SLACK_CHANNEL,
        text=message
    )
