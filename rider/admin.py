# from django.contrib import admin
# from django.utils import timezone
# from django.utils.html import format_html
#
# from notification.service import EmailManager
# from rider.forms import RiderActionForm
# from rider.models import (
#     ApprovedRider,
#     Commission,
#     Rider,
#     RiderCommission,
#     RiderDocument,
#     UnApprovedRider,
# )
# from rider.service import RiderService
#
#
# class RiderDocumentInline(admin.TabularInline):
#     model = RiderDocument
#     readonly_fields = ("type", "file_url_link", "number")
#     ordering = ("type",)
#     fields = ("file_url_link", "type", "number", "verified")
#     extra = 0
#
#     def file_url_link(self, instance):
#         if instance.file_url:
#             return format_html(
#                 '<a href="{}" target="_blank" download="">{}</a>',
#                 instance.file_url,
#                 instance.file_url,
#             )
#         else:
#             return ""
#
#     file_url_link.short_description = "File URL"  # type: ignore
#
#     def formfield_for_dbfield(self, *args, **kwargs):
#         formfield = super().formfield_for_dbfield(*args, **kwargs)
#
#         formfield.widget.can_delete_related = False
#         formfield.widget.can_change_related = False
#         formfield.widget.can_add_related = False
#
#         return formfield
#
#
# class RiderAdmin(admin.ModelAdmin):
#     form = RiderActionForm
#     search_fields = (
#         "user__first_name",
#         "user__last_name",
#         "vehicle_plate_number",
#         "vehicle_make",
#         "vehicle_model",
#     )
#     readonly_fields = (
#         "user",
#         "status",
#         "avatar_url",
#         "vehicle_plate_number",
#         "vehicle_color",
#         "vehicle",
#         "vehicle_make",
#         "vehicle_model",
#         "rider_status",
#         "on_duty",
#     )
#     list_display = ("get_name", "rider_status", "on_duty")
#     ordering = ("-created_at",)
#     exclude = (
#         "status_updates",
#         "operation_locations",
#         "state",
#         "created_by",
#         "deleted_by",
#         "updated_by",
#         "deleted_at",
#     )
#     inlines = [RiderDocumentInline]
#
#     def get_name(self, obj):
#         return obj.display_name
#
#     def rider_status(self, obj):
#         return obj.get_rider_status()
#
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         action = form.data.get("action")
#         action_reason = form.data.get("action_reason", "")
#
#         if action == "APPROVE_RIDER":
#             status_updates = obj.status_updates
#             status_updates.append({"status": "APPROVED", "date": str(timezone.now())})
#             obj.status_updates = status_updates
#             obj.status = "APPROVED"
#             obj.save()
#             RiderService.set_rider_avatar_with_passport(obj)
#             email_manager = EmailManager(
#                 "Your Documents Have Been Accepted",
#                 context={"display_name": obj.display_name},
#                 template="rider_accepted.html",
#             )
#             email_manager.send([obj.user.email])
#
#         elif action == "DISAPPROVE_RIDER":
#             status_updates = obj.status_updates
#             status_updates.append(
#                 {
#                     "status": "DISAPPROVED",
#                     "decline_reason": action_reason,
#                     "date": str(timezone.now()),
#                 }
#             )
#             obj.status_updates = status_updates
#             obj.status = "DISAPPROVED"
#             obj.save()
#             email_manager = EmailManager(
#                 "We Could Not Approve Your Documents",
#                 context={
#                     "display_name": obj.display_name,
#                     "decline_reason": action_reason,
#                 },
#                 template="rider_declined.html",
#             )
#             email_manager.send([obj.user.email])
#         elif action == "SUSPEND_RIDER":
#             status_updates = obj.status_updates
#             status_updates.append(
#                 {
#                     "status": "SUSPENDED",
#                     "suspend_reason": action_reason,
#                     "date": str(timezone.now()),
#                 }
#             )
#             obj.status_updates = status_updates
#             obj.status = "SUSPENDED"
#             obj.save()
#             email_manager = EmailManager(
#                 "Account Suspension",
#                 context={
#                     "display_name": obj.display_name,
#                     "suspend_reason": action_reason,
#                 },
#                 template="rider_suspended.html",
#             )
#             email_manager.send([obj.user.email])
#
#     def has_add_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def get_queryset(self, request):
#         return self.model.objects.exclude(user__state="DELETED")
#
#
# class ApprovedRiderAdmin(RiderAdmin):
#     def get_queryset(self, request):
#         return self.model.objects.filter(status="APPROVED").exclude(
#             user__state="DELETED"
#         )
#
#
# class UnApprovedRiderAdmin(RiderAdmin):
#     def get_queryset(self, request):
#         return (
#             self.model.objects.filter(status__in=["UNAPPROVED", "DISAPPROVED"])
#             .exclude(user__state="DELETED")
#             .order_by("-created_at")
#         )
#
#
# class RiderCommissionInline(admin.TabularInline):
#     model = RiderCommission
#     extra = 0
#     exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "rider":  # Assuming 'rider' is the ForeignKey field
#             kwargs["queryset"] = Rider.objects.exclude(user__state="DELETED")
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#     def get_queryset(self, request):
#         return self.model.objects.exclude(rider__user__state="DELETED").order_by(
#             "-created_at"
#         )
#
#
# class CommissionAdmin(admin.ModelAdmin):
#     search_fields = ("name", "note", "commission")
#     list_display = ("name", "commission")
#     ordering = ("-created_at",)
#     exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")
#     inlines = [RiderCommissionInline]
#
#
# admin.site.register(ApprovedRider, ApprovedRiderAdmin)
# admin.site.register(UnApprovedRider, UnApprovedRiderAdmin)
# admin.site.register(Rider, RiderAdmin)
# admin.site.register(Commission, CommissionAdmin)

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from notification.service import EmailManager
from rider.forms import RiderActionForm
from rider.models import Commission, Rider, RiderCommission, RiderDocument
from rider.service import RiderService


class RiderDocumentInline(TabularInline):
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


@admin.register(Rider)
class RiderAdmin(ModelAdmin):  # Use UnfoldAdmin instead of ModelAdmin
    inlines = [RiderDocumentInline]
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
        "rider_status",
        "on_duty",
    )
    list_display = ("get_name", "status", "on_duty")
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
    list_filter = ("status",)  # Add any additional filters if needed

    def get_name(self, obj):
        return obj.display_name

    def rider_status(self, obj):
        return obj.get_rider_status()

    rider_status.short_description = "Rider Status"  # type: ignore

    def get_rider_status(self, obj):
        return obj.get_rider_status()

    get_rider_status.short_description = "Rider Status"  # type: ignore

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        action = form.data.get("action")
        action_reason = form.data.get("action_reason", "")

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
                    "decline_reason": action_reason,
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
                    "decline_reason": action_reason,
                },
                template="rider_declined.html",
            )
            email_manager.send([obj.user.email])
        elif action == "SUSPEND_RIDER":
            status_updates = obj.status_updates
            status_updates.append(
                {
                    "status": "SUSPENDED",
                    "suspend_reason": action_reason,
                    "date": str(timezone.now()),
                }
            )
            obj.status_updates = status_updates
            obj.status = "SUSPENDED"
            obj.save()
            email_manager = EmailManager(
                "Account Suspension",
                context={
                    "display_name": obj.display_name,
                    "suspend_reason": action_reason,
                },
                template="rider_suspended.html",
            )
            email_manager.send([obj.user.email])

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return self.model.objects.exclude(user__state="DELETED")


class RiderCommissionInline(TabularInline):
    model = RiderCommission
    extra = 0
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "rider":  # Assuming 'rider' is the ForeignKey field
            kwargs["queryset"] = Rider.objects.exclude(user__state="DELETED")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return self.model.objects.exclude(rider__user__state="DELETED").order_by(
            "-created_at"
        )


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    search_fields = ("name", "note", "commission")
    list_display = ("name", "commission")
    ordering = ("-created_at",)
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")
    inlines = [RiderCommissionInline]
