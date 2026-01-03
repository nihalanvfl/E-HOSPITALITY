from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Show in list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

    # Add role in fieldsets (edit page)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    # Add role in add_fieldsets (create user page)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
