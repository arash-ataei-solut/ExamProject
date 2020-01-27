from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fields = ('profile_username', 'full_name')
    search_fields = ('profile_username', 'profile_first_name', 'profile_last_name')


admin.site.register(Profile, ProfileAdmin)
