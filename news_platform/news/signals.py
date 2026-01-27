from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Tovar
from .tasks import send_notifications

@receiver(m2m_changed, sender=Tovar.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_notifications.delay(instance.id)