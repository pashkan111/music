from django.contrib import admin
from .models import *
from .services.base_auth import User


@admin.register(User)
class AdminAuthUser(admin.ModelAdmin):
    list_display = (
        'email', 'country', 'city', 'display_name', 'avatar'
    )
    list_display_links = ('email', )
