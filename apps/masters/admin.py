from django.contrib import admin

from apps.masters.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    search_fields = ('name',)


# Register your models here.
admin.site.register(Category, CategoryAdmin)