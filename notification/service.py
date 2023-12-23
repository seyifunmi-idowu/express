from notification.models import UserNotification


class OneSignalService:
    @classmethod
    def add_user_one_signal(cls, user, one_signal_id, **kwargs):
        return UserNotification.objects.create(
            user=user, one_signal_id=one_signal_id, **kwargs
        )

    @classmethod
    def get_user_notification(cls, **kwargs):
        return UserNotification.objects.filter(**kwargs)
