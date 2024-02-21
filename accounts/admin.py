from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import Profile
from projects.models import Project, Solution

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'profile'
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

class ProjectInline(admin.TabularInline):
    model = Project
    can_delete = False
    verbose_name = 'project'
    verbose_name_plural = 'projects'

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = (ProjectInline, )

# Re-register User model to include Profiles in the admin page
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Profile, ProfileAdmin)