from django.contrib import admin, messages
from django.utils.html import format_html

from order.forms import VehicleAdminForm
from order.models import Order, Vehicle
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
            messages.info(request, f"Total Price for selected vehicles: {price}")
        else:
            super().save_model(request, obj, form, change)


class OrderAdmin(admin.ModelAdmin):
    search_fields = ("order_id", "status")
    list_display = ("order_id", "customer", "rider", "status", "distance", "created_at")
    ordering = ["created_at"]
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
        "pickup_location",
        "delivery_number",
        "delivery_contact_name",
        "delivery_location",
        "delivery_time",
        "created_at",
        "updated_by",
        "updated_at",
    )
    fields = (
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
        "pickup_location",
        "delivery_number",
        "delivery_contact_name",
        "delivery_location",
        "delivery_time",
        "order_timeline",
        "created_at",
        "updated_by",
        "updated_at",
    )

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Vehicle, VehiclesAdmin)
admin.site.register(Order, OrderAdmin)
