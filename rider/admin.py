from django.contrib import admin
from django.utils.html import format_html

from rider.forms import RiderActionForm
from rider.models import ApprovedRider, Rider, RiderDocument, UnApprovedRider


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
        "avatar_url",
        "vehicle_plate_number",
        "vehicle_color",
        "vehicle",
        "vehicle_make",
        "vehicle_model",
        "city",
        "rider_status",
    )
    list_display = ("get_name", "rider_status")
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
        if action == "APPROVE_RIDER":
            obj.status = "APPROVED"
            obj.save()
        elif action == "DISAPPROVE_RIDER":
            obj.status = "UNAPPROVED"
            obj.save()
        elif action == "SUSPEND_RIDER":
            obj.status = "SUSPENDED"
            obj.save()

    def has_add_permission(self, request, obj=None):
        return False


class ApprovedRiderAdmin(RiderAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(status="APPROVED")


class UnApprovedRiderAdmin(RiderAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(status="UNAPPROVED")


admin.site.register(ApprovedRider, ApprovedRiderAdmin)
admin.site.register(UnApprovedRider, UnApprovedRiderAdmin)
admin.site.register(Rider, RiderAdmin)
