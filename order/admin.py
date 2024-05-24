from django.contrib import admin, messages
from django.utils.html import format_html

from order.forms import OrderAdminForm, VehicleAdminForm
from order.models import Order, OrderTimeline, PendingOrder, Vehicle
from order.service import OrderService


class VehiclesAdmin(admin.ModelAdmin):
    form = VehicleAdminForm
    search_fields = ("name", "status")
    readonly_fields = ("file_url_link", "created_at", "updated_by", "updated_at")
    list_display = ("name", "status")
    ordering = ["name"]
    fields = (
        "name",
        "status",
        "note",
        "start_date",
        "end_date",
        "base_fare",
        "km_5_below_fare",
        "km_5_above_fare",
        "price_per_minute",
        "file_url_link",
        "created_at",
        "updated_at",
        "updated_by",
        "action",
        "start_address",
        "end_address",
        "vehicle_image",
    )

    def file_url_link(self, instance):
        if instance.file_url:
            return format_html(
                '<a href="{}" target="_blank" download="">{}</a>',
                instance.file_url,
                instance.file_url,
            )
        else:
            return ""

    file_url_link.short_description = "vehicle image url"  # type: ignore

    def save_model(self, request, obj, form, change):
        action = form.cleaned_data.get("action", "")
        if action == "CHANGE_VEHICLE_IMAGE":
            vehicle_image = form.cleaned_data.get("vehicle_image", None)
            super().save_model(request, obj, form, change)
            if vehicle_image:
                from helpers.s3_uploader import SuggestedImageUploader

                previous_file_url = obj.file_url
                if previous_file_url:
                    SuggestedImageUploader().hard_delete_object(previous_file_url)
                s3_uploader = SuggestedImageUploader(
                    append_folder="/available-vehicles"
                )
                file_url = s3_uploader.upload_file_object(
                    file_object=vehicle_image.file,
                    file_name=vehicle_image.name,
                    use_random_key=True,
                )
                obj.file_url = file_url
                obj.updated_by = request.user
                messages.info(
                    request,
                    "The Available Vehicle image was changed successfully. You may edit it again below.",
                )
        elif action == "CHECK_PRICE":
            start_address = form.cleaned_data.get("start_address")
            end_address = form.cleaned_data.get("end_address")
            price = OrderService.admin_get_location_price(
                obj.id, start_address, end_address
            )
            if price is None:
                messages.info(
                    request,
                    "Unable to process, please check that the address is correct",
                )
            else:
                messages.info(request, f"Total Price for selected vehicles: {price}")

        else:
            super().save_model(request, obj, form, change)


class OrderTimelineInline(admin.TabularInline):
    model = OrderTimeline
    readonly_fields = ("status", "date", "proof_link", "reason")
    ordering = ("created_at",)
    fields = ("status", "date", "proof_link", "reason")
    extra = 0

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield

    def date(self, instance):
        return instance.get_created_at()

    def proof_link(self, instance):
        if instance.proof_url:
            return format_html(
                '<a href="{}" target="_blank" download="">{}</a>',
                instance.proof_url,
                instance.proof_url,
            )
        else:
            return ""

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# class OrderForFilter(admin.SimpleListFilter):
#     title = _('Order for')
#     parameter_name = 'order_for'
#
#     def lookups(self, request, model_admin):
#         from django.utils.translation import gettext_lazy as _
#         return (
#             ('customer', _('Customer order')),
#             ('business', _('Business order')),
#         )
#
#     def queryset(self, request, queryset):
#         if self.value() == 'customer':
#             return queryset.filter(customer__isnull=False)
#         elif self.value() == 'business':
#             return queryset.filter(business__isnull=False)


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    inlines = [OrderTimelineInline]
    search_fields = ("order_id", "status")
    list_display = (
        "order_id",
        "customer",
        "business",
        "rider",
        "status",
        "distance",
        "created_at",
    )
    ordering = ["-created_at"]
    list_filter = ("order_by", "status")
    readonly_fields = (
        "customer",
        "rider",
        "vehicle",
        "status",
        "payment_method",
        "payment_by",
        "paid",
        "total_amount",
        "tip_amount",
        "fele_amount",
        "paid_fele",
        "pickup_number",
        "pickup_contact_name",
        "pickup_name",
        "pickup_location",
        "pickup_location_longitude",
        "pickup_location_latitude",
        "delivery_number",
        "delivery_contact_name",
        "delivery_name",
        "delivery_location",
        "delivery_time",
        "delivery_location_longitude",
        "delivery_location_latitude",
        "order_meta_data",
        "created_at",
        "updated_by",
        "updated_at",
    )
    fields = (
        "action",
        "reason",
        "customer",
        "rider",
        "vehicle",
        "status",
        "payment_method",
        "payment_by",
        "paid",
        "total_amount",
        "tip_amount",
        "fele_amount",
        "paid_fele",
        "pickup_number",
        "pickup_contact_name",
        "pickup_name",
        "pickup_location",
        "pickup_location_longitude",
        "pickup_location_latitude",
        "delivery_number",
        "delivery_contact_name",
        "delivery_name",
        "delivery_location",
        "delivery_time",
        "delivery_location_longitude",
        "delivery_location_latitude",
        "order_meta_data",
        "created_at",
        "updated_by",
        "updated_at",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        order = self.model.objects.exclude(customer__user__state="DELETED")
        order = order.exclude(rider__user__state="DELETED")
        order = order.exclude(business__user__state="DELETED")
        return order

    def save_model(self, request, obj, form, change):
        from order.service import OrderService

        action = form.cleaned_data.get("action", "")
        if action == "CANCEL_ORDER":
            reason = form.cleaned_data.get("reason", "")
            OrderService.add_order_timeline_entry(
                obj, "ORDER_CANCELLED", **{"cancelled_by": "admin", "reason": reason}
            )
            obj.status = "ORDER_CANCELLED"
            obj.save()
        else:
            super().save_model(request, obj, form, change)


class PendingOrderAdmin(OrderAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(
            status__in=["PENDING", "PROCESSING_ORDER", "PENDING_RIDER_CONFIRMATION"]
        )


admin.site.register(Vehicle, VehiclesAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PendingOrder, PendingOrderAdmin)
