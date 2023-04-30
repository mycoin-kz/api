from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserAdmin(UserAdmin):
    # ordering = ['email', ]
    # list_display = ['email', ]
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("email", "name", "is_staff", "profile_pic")
    # list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("name", "email")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
