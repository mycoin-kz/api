from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from main_module.models import Watchlist


class WatchlistInline(admin.TabularInline):
    model = Watchlist
    extra = 1  # Number of empty forms to display


class CustomUserAdmin(UserAdmin):
    inlines = (WatchlistInline,)
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
    search_fields = ("name", "email")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
