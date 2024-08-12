from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser, Reader, Librarian

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_display_links = ('username', 'email')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    readonly_fields = ('id',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'username', 'email'),
        }),
        ('Security', {
            'fields': ('password',),
        }),
        ('Other Info', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'last_login'),
        }),
    )
    add_fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'username', 'email'),
        }),
        ('Security', {
            'fields': ('password1', 'password2'),
        }),
        ('Other Info', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'last_login'),
        }),
    )


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id')
    search_fields = ('user__username', 'employee_id')


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'address')
    search_fields = ('user__username', 'first_name', 'last_name', 'address')
