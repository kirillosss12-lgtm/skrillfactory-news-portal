from django.contrib.auth.models import Group
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def add_to_common_group(request, user, **kwargs):
    common_group, created = Group.objects.get_or_create(name='common')
    user.groups.add(common_group)