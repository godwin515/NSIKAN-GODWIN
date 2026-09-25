from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import StudentProfile


@receiver(post_save, sender=StudentProfile)
def set_default_password_if_none(sender, instance, created, **kwargs):
    """If a newly-created StudentProfile's User has no usable password,
    set a default one and print it to the console."""
    if not created:
        return

    user = instance.user
    if not user.has_usable_password():
        # Build a default password from the admission number, e.g. "NH2026-001"
        default_pw = instance.admission_number.replace('/', '').replace('-', '')
        user.set_password(default_pw)
        user.save(update_fields=['password'])
        print(f"[student] Default password for {instance.admission_number} set to: {default_pw}")