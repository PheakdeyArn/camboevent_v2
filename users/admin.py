from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, CommentEvent

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

from mptt.admin import MPTTModelAdmin



class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': (
            'email',
            'first_name',
            'last_name',
            # 'phone_number',
            'job',
            'password',
            'last_login'
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = (
        'email',
        'first_name',
        'last_name',
        # 'phone_number',
        'job',
        'ip_address',
        'is_staff',
        'last_login'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    # model = User
    # menu_label = "Users"
    # menu_icon = "placeholder"
    # menu_order = 290
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    # list_display = ("email", "first_name", "last_name", "phone_number",)
    # search_fields = ("email", "first_name", "last_name", "phone_number",)


admin.site.register(User, UserAdmin)
# modeladmin_register(UserAdmin)
admin.site.register(CommentEvent, MPTTModelAdmin)
