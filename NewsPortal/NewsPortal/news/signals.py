from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from .models import *
from .tasks import mail_from_subscribers


# @receiver(signal=m2m_changed, sender=PostCategory,)
# def mail_from_subscribers(instance, action, **kwargs):
