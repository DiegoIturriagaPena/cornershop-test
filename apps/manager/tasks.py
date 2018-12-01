from __future__ import absolute_import

from backend.celery import app
from .notifiers import send_email_notification, send_slack_notification


@app.task(name='mail_notification_task', bind=True)
def email_notification(self, uuid_notification):
    send_email_notification(uuid_notification)
    return self.request.id


@app.task(name='slack_notification_task', bind=True)
def slack_notification(self, uuid_notification):
    send_slack_notification(uuid_notification)
    return self.request.id
