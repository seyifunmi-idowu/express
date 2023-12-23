from django.contrib import admin

from notification.models import UserNotification


class UserNotificationAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "one_signal_id", "external_id")
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")


admin.site.register(UserNotification, UserNotificationAdmin)
