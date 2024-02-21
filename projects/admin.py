from django.contrib import admin

from projects.models import Project, Solution

# Register your models here.
admin.site.register((Project, Solution))