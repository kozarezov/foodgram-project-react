from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Настройки админ панели для User."""

    list_display = ('pk', 'username',
                    'email', 'first_name',
                    'last_name', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'
