from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from authentication.forms import CreateUserForm
from authentication.models import User
from helpers.admin_helpers import BaseModelAdmin


class CustomUserAdmin(BaseModelAdmin, UserAdmin):
    actions = ["delete_user"]
    model = User
    list_display = ("first_name", "last_name", "email", "is_staff")
    list_filter = ("first_name", "last_name", "email", "is_staff")
    readonly_fields = ("deleted_at", "email_verified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "user_types",
                    "email",
                    "password",
                    "email_verified",
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
    search_fields = ("id", "first_name", "last_name", "email", "phone_number")
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


admin.site.register(User)
