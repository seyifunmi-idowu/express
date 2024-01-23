from typing import Dict, List

import sendgrid
from django.conf import settings
from django.db.models import Q
from django.template.loader import get_template
from sendgrid.helpers.mail import Content, Email, From, Mail, Subject, To

from helpers.logger import CustomLogging
from helpers.onesignal_integration import OneSignalIntegration
from notification.models import UserNotification


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
        return UserNotification.objects.create(
            user=user, one_signal_id=one_signal_id, **kwargs
        )

    @classmethod
    def get_user_notification(cls, **kwargs):
        return UserNotification.objects.filter(**kwargs)

    @classmethod
    def add_user_for_sms_notification(cls, user):
        user_notification = UserNotification.objects.filter(
            Q(meta_data__contains=[{"phone_number": user.phone_number}])
        )
        if user_notification and user_notification.first().subscription_id:
            return True

        response = OneSignalIntegration.add_sms_device(
            user.phone_number, user.id, user.first_name, user.last_name
        )
        subscription_id = response["id"]
        UserNotification.objects.create(
            user=user,
            subscription_id=subscription_id,
            notification_type="SMS",
            meta_data={"phone_number": user.phone_number},
        )
        return True

    @classmethod
    def delete_user_from_sms_notification(cls, user, message):
        user_notification = cls.get_user_notification(
            user=user, notification_type="SMS"
        ).first()
        phone_number = user_notification.get_phone_number()
        response = OneSignalIntegration.send_sms_notification(phone_number, message)
        return response.get("success", False)

    @classmethod
    def send_sms_message(cls, user, message):
        user_notification = UserNotification.objects.filter(
            user=user, notification_type="SMS"
        ).first()
        phone_number = user_notification.get_phone_number()
        response = SmsManager.send_sms(phone_number, message)
        return response.get("success", False)
