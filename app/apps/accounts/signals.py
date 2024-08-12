from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.accounts.models import Reader

User = get_user_model()


@receiver(post_save, sender=User)
def create_reader_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        if not hasattr(instance, 'reader'):
            Reader.objects.create(user=instance, address='')
