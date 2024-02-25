from datetime import datetime
from typing import Dict, List

import sendgrid
from django.conf import settings
from django.template.loader import get_template
from rest_framework import status
from sendgrid.helpers.mail import Content, Email, From, Mail, Subject, To

from helpers.exceptions import CustomAPIException
from helpers.logger import CustomLogging
from helpers.onesignal_integration import OneSignalIntegration
from notification.models import Notification, UserNotification


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
        user_notification = UserNotification.objects.filter(
            one_signal_id=one_signal_id, status="ACTIVE", user=user
        ).first()
        if user_notification:
            return user_notification

        actual_user_notification = None
        user_notifications = cls.get_one_signal(one_signal_id=one_signal_id)
        for user_notification in user_notifications:
            if user_notification.user == user:
                user_notification.status = "ACTIVE"
                actual_user_notification = user_notification
            else:
                user_notification.status = "INACTIVE"
            user_notification.save()
        if actual_user_notification:
            return actual_user_notification
        else:
            return UserNotification.objects.create(
                user=user, one_signal_id=one_signal_id, **kwargs
            )

    @classmethod
    def get_one_signal(cls, one_signal_id):
        return UserNotification.objects.filter(one_signal_id=one_signal_id)

    @classmethod
    def get_user_one_signal(cls, user):
        return UserNotification.objects.filter(user=user, status="ACTIVE")

    @classmethod
    def send_sms_message(cls, user, message):
        phone_number = user.phone_number
        response = SmsManager.send_sms(phone_number, message)
        return response.get("success", False)

    @classmethod
    def send_push_notification(cls, user, title, message, add_to_notification=True):
        user_notification = cls.get_user_one_signal(user).first()
        if user_notification is not None:
            one_signal_id = user_notification.one_signal_id
            formatted_message = message[:100] + "..." if len(message) > 50 else message
            OneSignalIntegration.send_push_notification(
                [one_signal_id], title, formatted_message
            )

        add_to_notification and cls.add_user_notification(user, title, message)

    @classmethod
    def send_collective_push_notification(
        cls, users, title, message, add_to_notification=True
    ):
        subscription_list = []
        for user in users:
            user_notification = cls.get_user_one_signal(user).first()
            if user_notification is not None:
                subscription_list.append(user_notification.one_signal_id)

        formatted_message = message[:100] + "..." if len(message) > 50 else message
        OneSignalIntegration.send_push_notification(
            subscription_list, title, formatted_message
        )

        if add_to_notification:
            for user in users:
                cls.add_user_notification(user, title, message)

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
