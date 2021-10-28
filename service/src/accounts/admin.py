from django.contrib import admin
from .models import *


@admin.register(AuthUser)
class AdminAuthUser(admin.ModelAdmin):
    list_display = (
        'email', 'country', 'city', 'display_name', 'avatar'
    )
    list_display_links = ('email', )