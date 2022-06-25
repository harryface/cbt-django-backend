from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models.user import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name',
                    'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name',
                           'last_name', 'password', 'email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('AlexaBitcoins Permissions', {'fields': ()}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# @admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'first_name', 'last_name', 'email', 'unique_id', 'referred_by', 'rank', 'banned')
    list_filter = ('rank', 'banned')
    actions_selection_counter = True
    actions = ['ban_user']

    @admin.action(description='Ban Selected Users')
    def ban_user(self, request, queryset):
        queryset.update(banned=True)


# @admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'receiver')
    search_fields = ('body', 'title')


admin.site.unregister(Group)
