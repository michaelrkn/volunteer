from django import template
from core.views import profile_check

register = template.Library()


tiers=[{'goal':50000,'name':'Tier 1'},{'goal':100000,'name':'Tier 2'},{'goal':250000,'name':'Tier 3'},{'goal':500000,'name':'Tier 4'}]


@register.filter
def user_has_profile(user):
    return profile_check(user)

@register.filter
def user_has_phone(user):
    return not user.volunteer.phone is None

@register.filter
def get_tier(user,prop):
    num=user.volunteer.outvote_texts
    for tier in tiers:
        if tier['goal']>=num:
            return tier[prop]
    return {'goal':"The sky's the limit!",'name':'Tier 5'}[prop]

@register.filter
def get_tier_progress(user):
    num=user.volunteer.outvote_texts
    for tier in tiers:
        if tier['goal']>=num:
            return int(100*num/tier['goal'])
    return int(100*num/tiers[-1]['goal'])