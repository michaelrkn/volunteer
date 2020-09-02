from django import template
from core.views import profile_check

register = template.Library()

@register.filter
def user_has_profile(user):
    return profile_check(user)