from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_username_from_id(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return 'Unknown'