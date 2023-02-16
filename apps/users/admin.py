from django.contrib import admin

from apps.users import models

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'avatar', 'mobile')
    search_fields = ('last_name', 'first_name')

admin.site.register(models.UserProfile, UserProfileAdmin)