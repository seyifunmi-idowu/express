from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from authentication.forms import CreateUserForm
from authentication.models import User, UserActivity
from helpers.admin_helpers import BaseModelAdmin


class CustomUserAdmin(BaseModelAdmin, UserAdmin):
    actions = ["delete_user"]
    model = User
    list_display = ("first_name", "last_name", "email", "user_type", "is_staff")
    list_filter = ("first_name", "last_name", "user_type")
    readonly_fields = ("deleted_at", "email_verified", "phone_verified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "user_type",
                    "email",
                    "password",
                    "email_verified",
                    "phone_verified",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "user_type",
    )
    ordering = ("first_name", "last_name", "email")
    add_form = CreateUserForm

    def get_queryset(self, request):
        return self.model.objects.filter(state="ACTIVE")

    def delete_user(self, request, queryset):
        for obj in queryset:
            email = obj.email
            obj.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"User with email => {email}, deleted successfully",
            )


class UserActivityAdmin(admin.ModelAdmin):
    model = UserActivity
    ordering = ["-created_at"]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__phone_number",
        "id",
        "session_id",
    ]
    list_display = ("user", "category", "action")
    list_filter = ("category", "level")

    fields = (
        "session_id",
        "level",
        "action",
        "category",
        "user",
        "rider",
        "customer",
        "context",
    )

    readonly_fields = (
        "session_id",
        "level",
        "action",
        "category",
        "user",
        "rider",
        "customer",
        "context",
    )

    def consumer_name(self, obj):
        return obj.consumer.user.display_name

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
