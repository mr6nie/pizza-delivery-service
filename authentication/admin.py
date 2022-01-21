from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    model = User
    list_display = [
        "id",
        "email",
        "username",
        "phone_number",
        "is_staff",
        "is_active",
    ]
    list_display_links = ["id", "email"]
    list_filer = [
        "email",
        "username",
        "phone_number",
        "is_staff",
        "is_active",
    ]


admin.site.register(User, UserAdmin)
