from django.contrib import admin
from user.forms import CustomUserCreationForm

from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (
            'Individuelle Daten',
            {
                'fields':(
                    'custom',
                    'phone',
                    'adress',
                )
            }
        ),
    *UserAdmin.fieldsets,
    )

