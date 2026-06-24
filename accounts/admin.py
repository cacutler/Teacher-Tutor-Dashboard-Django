from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Status, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("middle_name", "birthdate", "gender", "statuses")}),
    )
    filter_horizontal = UserAdmin.filter_horizontal + ("statuses",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("name",)
