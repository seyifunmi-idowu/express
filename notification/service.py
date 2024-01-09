from django.db.models import Q

from helpers.onesignal_integration import OneSignalIntegration
from notification.models import UserNotification


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
