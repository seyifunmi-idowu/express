from django.contrib import admin

from notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")


admin.site.register(Notification, NotificationAdmin)
