from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'gender', 'age', 'city')

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('age', 'gender', 'city', 'bio', 'photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('age', 'gender', 'city', 'bio', 'photo')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)