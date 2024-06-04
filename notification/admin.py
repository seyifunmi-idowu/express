from django.contrib import admin

from notification.forms import NotificationActionForm
from notification.models import Notification, UserNotification
from notification.service import NotificationService


class NotificationAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
    form = NotificationActionForm
    readonly_fields = ("created_at",)
    exclude = (
        "meta_data",
        "state",
        "created_by",
        "deleted_by",
        "updated_by",
        "deleted_at",
    )
    list_display = ("user", "title", "created_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        delivery_type = form.data.get("delivery_type")

        if not change:
            if delivery_type == "PUSH":
                NotificationService.send_push_notification(
                    user=obj.user,
                    title=obj.title,
                    message=obj.message,
                    add_to_notification=False,
                )


admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserNotification)
