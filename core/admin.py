from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import Volunteer, Friend


class VolunteerInline(admin.StackedInline):
    model = Volunteer
    can_delete = False
    verbose_name_plural = 'volunteer'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (VolunteerInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)




class FriendsInline(admin.TabularInline):
    model = Friend


@admin.register(Volunteer)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("slug","user", "_friends")

    inlines = [
        FriendsInline
    ]

    def _friends(self, obj):
        return obj.friends.all().count()


admin.site.register(Friend)