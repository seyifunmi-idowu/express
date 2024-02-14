from datetime import datetime
from typing import Dict, List

import sendgrid
from django.conf import settings
from django.template.loader import get_template
from rest_framework import status
from sendgrid.helpers.mail import Content, Email, From, Mail, Subject, To

from helpers.exceptions import CustomAPIException
from helpers.logger import CustomLogging
from notification.models import Notification, ThirdPartyNotification


class EmailManager:
    sender_email = settings.SENDER_EMAIL
    sender_name = settings.SENDER_NAME
    general_template = "templated_email/general.email"
    api_key = settings.SENDGRID_API_KEY

    def __init__(self, subject, context: Dict, template=None):
        self.template = template
        self.context = context
        self.subject = subject
        self.from_email = Email(self.sender_email, self.sender_name)
        self.html_content = get_template(self.template).render(self.context)
        self.email_content = Content("text/html", self.html_content)

    # @shared_task
    def _send_email(self, message):
        # TODO: we would need to put this in a task
        sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
        sg.client.mail.send.post(request_body=message.get())

    def send(self, recipient_emails: List[str]):
        email_to_list = [To(email=email_to) for email_to in recipient_emails]
        try:
            message = Mail()
            message.to = email_to_list
            message.from_email = From(email=self.sender_email, name=self.sender_name)
            message.subject = Subject(self.subject)

            message.content = [self.email_content]
            self._send_email(message)
            return True

        except Exception as e:
            extra = {"errors": str(e)}
            CustomLogging.error(f"cannot send mail to {recipient_emails}", extra=extra)
            return False


class SmsManager:
    secret_key = settings.TERMII_API_KEY
    sms_from = settings.TERMII_SMS_FROM
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    base_url = "https://api.ng.termii.com/"

    @classmethod
    def send_sms(cls, phone_number, message):
        import requests

        url = f"{cls.base_url}/api/sms/send"
        data = {
            "to": [phone_number],
            "sms": message,
            "api_key": cls.secret_key,
            "channel": "dnd",
            "from": cls.sms_from,
            "type": "plain",
        }
        response = requests.post(url, headers=cls.headers, json=data)
        return response.json()


class NotificationService:
    @classmethod
    def add_user_one_signal(cls, user, one_signal_id, **kwargs):
        return ThirdPartyNotification.objects.create(
            user=user, one_signal_id=one_signal_id, **kwargs
        )

    @classmethod
    def get_user_one_signal(cls, one_signal_id):
        return ThirdPartyNotification.objects.filter(one_signal_id=one_signal_id)

    @classmethod
    def send_sms_message(cls, user, message):
        phone_number = user.phone_number
        response = SmsManager.send_sms(phone_number, message)
        return response.get("success", False)

    @classmethod
    def add_user_notification(cls, user, title, message):
        return Notification.objects.create(user=user, title=title, message=message)

    @classmethod
    def get_user_notifications(cls, user):
        return Notification.objects.filter(user=user).order_by("-created_at")

    @classmethod
    def opened_notification(cls, notification_id, user):
        notification = Notification.objects.filter(
            id=notification_id, user=user
        ).first()
        if notification is None:
            raise CustomAPIException(
                "Notification not found.", status.HTTP_404_NOT_FOUND
            )
        notification.opened = True
        meta_data = notification.meta_data
        notification.meta_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **meta_data,
        }
        notification.save()
        return True
