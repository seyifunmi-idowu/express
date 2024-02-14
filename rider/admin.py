from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from notification.service import EmailManager
from rider.forms import RiderActionForm
from rider.models import ApprovedRider, Rider, RiderDocument, UnApprovedRider
from rider.service import RiderService


class RiderDocumentInline(admin.TabularInline):
    model = RiderDocument
    readonly_fields = ("type", "file_url_link", "number")
    ordering = ("type",)
    fields = ("file_url_link", "type", "number", "verified")
    extra = 0

    def file_url_link(self, instance):
        if instance.file_url:
            return format_html(
                '<a href="{}" target="_blank" download="">{}</a>',
                instance.file_url,
                instance.file_url,
            )
        else:
            return ""

    file_url_link.short_description = "File URL"  # type: ignore

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield


class RiderAdmin(admin.ModelAdmin):
    form = RiderActionForm
    search_fields = (
        "user__first_name",
        "user__last_name",
        "vehicle_plate_number",
        "vehicle_make",
        "vehicle_model",
    )
    readonly_fields = (
        "user",
        "status",
        "avatar_url",
        "vehicle_plate_number",
        "vehicle_color",
        "vehicle",
        "vehicle_make",
        "vehicle_model",
        "city",
        "rider_status",
        "on_duty",
    )
    list_display = ("get_name", "rider_status", "on_duty")
    ordering = ("-created_at",)
    exclude = (
        "status_updates",
        "operation_locations",
        "state",
        "created_by",
        "deleted_by",
        "updated_by",
        "deleted_at",
    )
    inlines = [RiderDocumentInline]

    def get_name(self, obj):
        return obj.display_name

    def rider_status(self, obj):
        return obj.get_rider_status()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        action = form.data.get("action")
        decline_reason = form.data.get("decline_reason", "")

        if action == "APPROVE_RIDER":
            status_updates = obj.status_updates
            status_updates.append({"status": "APPROVED", "date": str(timezone.now())})
            obj.status_updates = status_updates
            obj.status = "APPROVED"
            obj.save()
            RiderService.set_rider_avatar_with_passport(obj)
            email_manager = EmailManager(
                "Your Documents Have Been Accepted",
                context={"display_name": obj.display_name},
                template="rider_accepted.html",
            )
            email_manager.send([obj.user.email])

        elif action == "DISAPPROVE_RIDER":
            status_updates = obj.status_updates
            status_updates.append(
                {
                    "status": "DISAPPROVED",
                    "decline_reason": decline_reason,
                    "date": str(timezone.now()),
                }
            )
            obj.status_updates = status_updates
            obj.status = "DISAPPROVED"
            obj.save()
            email_manager = EmailManager(
                "We Could Not Approve Your Documents",
                context={
                    "display_name": obj.display_name,
                    "decline_reason": decline_reason,
                },
                template="rider_declined.html",
            )
            email_manager.send([obj.user.email])
        elif action == "SUSPEND_RIDER":
            status_updates = obj.status_updates
            status_updates.append(
                {
                    "status": "SUSPENDED",
                    "decline_reason": decline_reason,
                    "date": str(timezone.now()),
                }
            )
            obj.status_updates = status_updates
            obj.status = "SUSPENDED"
            obj.save()

    def has_add_permission(self, request, obj=None):
        return False


class ApprovedRiderAdmin(RiderAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(status="APPROVED")


class UnApprovedRiderAdmin(RiderAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(status__in=["UNAPPROVED", "DISAPPROVED"])


admin.site.register(ApprovedRider, ApprovedRiderAdmin)
admin.site.register(UnApprovedRider, UnApprovedRiderAdmin)
admin.site.register(Rider, RiderAdmin)
