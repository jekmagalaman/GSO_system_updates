from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields shown in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'unit', 'is_staff')

    # Filters shown in the admin list view
    list_filter = ('role', 'unit', 'is_staff', 'is_superuser')

    # Fields shown in the user detail/edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role info', {'fields': ('role', 'unit')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields used when creating a new user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'unit', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Register your custom User model with the custom admin
admin.site.register(User, UserAdmin)
