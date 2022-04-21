from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm, CustomUserChangeForm
from .models import (CustomUser,
                     Employee,
                     Team,
                     Reservation,
                     Comments,
                     Services)


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(Reservation)
admin.site.register(Comments)
admin.site.register(Services)
