from typing import Dict, List

import sendgrid
from django.conf import settings
from django.template.loader import get_template
from sendgrid.helpers.mail import Content, Email, From, Mail, Subject, To
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from helpers.logger import CustomLogging


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


class SMSManager:
    def __init__(self):
        self.account_sid = settings.ACCOUNT_SID
        self.auth_token = settings.AUTH_TOKEN
        self.verify_sid = settings.VERIFY_SID
        self.sms_from = settings.SMS_FROM
        self.client = Client(self.account_sid, self.auth_token)

    def send_verification_code(self, verified_number, custom_message=None):
        try:
            verification = self.client.verify.v2.services(
                self.verify_sid
            ).verifications.create(
                to=verified_number, channel="sms", custom_message=custom_message
            )

            # sample status "pending", "approved"
            return verification.status
        except TwilioRestException as e:
            extra = {"errors": str(e)}
            CustomLogging.error(
                "Error occurred while sending twillio verification code", extra=extra
            )
            return {"status": "error", "message": e.msg}

    def verify_verification_code(self, verified_number, code):
        try:
            verification_check = self.client.verify.v2.services(
                self.verify_sid
            ).verification_checks.create(to=verified_number, code=code)

            # sample status "pending", "approved"
            return verification_check.status
        except TwilioRestException as e:
            extra = {"errors": str(e)}
            CustomLogging.error(
                "Error occurred while verifying twillio code", extra=extra
            )
            return {"status": "error", "message": e.msg}

    def send_message(self, verified_number, message):
        try:
            message = self.client.messages.create(
                body=message, from_=self.sms_from, to=verified_number
            )

            return message.sid
        except TwilioRestException as e:
            extra = {"errors": str(e)}
            CustomLogging.error(
                f"Error occurred while sending message {str(e)}", extra=extra
            )
            message = e.msg
            if message.startswith("Unable to create record:"):
                message = message[24:]
            return {"status": "error", "message": message}
