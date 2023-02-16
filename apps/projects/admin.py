from django.contrib import admin

from apps.projects.models import Project


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url', 'category')
    search_fields = ('name', 'category__name')


admin.site.register(Project, ProjectAdmin)